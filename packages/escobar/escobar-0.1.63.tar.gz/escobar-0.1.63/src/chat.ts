import { JupyterFrontEnd } from '@jupyterlab/application';

import { Widget } from '@lumino/widgets';
import { Message } from '@lumino/messaging';
import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { VoittaToolRouter } from "./voitta/voittaServer";
import { initPythonBridge, callPython, registerFunction, get_ws, voittal_call_log, stopped_messages, PYTHON_CALL_EVENTS } from './voitta/pythonBridge_browser'

import { get_tools } from "./integrations/jupyter_integrations"

import { createEscobarSplitButton, createTopButtons } from "./js/ui_elements"
import { createSettingsPage } from "./js/setting_page"
import { MessageHandler, ResponseMessage, IChatSettings } from './messageHandler';
import { jsonrepair } from 'jsonrepair';

import { INotebookTracker } from '@jupyterlab/notebook';

import { functions } from "./integrations/jupyter_integrations"

import { IDebugger } from '@jupyterlab/debugger';

/**
 * Get the JupyterHub username from the client side
 * 
 * @returns An object containing the username and a flag indicating if it's from JupyterHub
 */
function getJupyterHubUsername(): { username: string, fromJupyterHub: boolean } {
  // Method 1: Check URL pattern - most reliable in JupyterHub
  // JupyterHub URLs typically follow the pattern: /user/{username}/lab/...
  const hubUserRegex = /\/user\/([^\/]+)\//;

  // First try with the pathname
  const pathname = window.location.pathname;
  const hubUserMatch = pathname.match(hubUserRegex);

  if (hubUserMatch && hubUserMatch[1]) {
    // Make sure to decode the username to handle special characters like @ in email addresses
    const decodedUsername = decodeURIComponent(hubUserMatch[1]);
    // Successfully found username from URL
    return { username: decodedUsername, fromJupyterHub: true };
  }

  // If pathname didn't work, try with the full URL
  const fullUrl = window.location.href;
  const fullUrlMatch = fullUrl.match(hubUserRegex);

  if (fullUrlMatch && fullUrlMatch[1]) {
    // Make sure to decode the username to handle special characters like @ in email addresses
    const decodedUsername = decodeURIComponent(fullUrlMatch[1]);
    // Successfully found username from full URL
    return { username: decodedUsername, fromJupyterHub: true };
  }

  // Method 2: Check for JupyterHub data in the page config
  try {
    // JupyterLab stores config data in a script tag with id jupyter-config-data
    const configElement = document.getElementById('jupyter-config-data');
    if (configElement && configElement.textContent) {
      const config = JSON.parse(configElement.textContent);

      // JupyterHub might store user info in different properties
      if (config.hubUser) {
        // Found username in page config
        return { username: config.hubUser, fromJupyterHub: true };
      }

      if (config.hubUsername) {
        // Found username in page config
        return { username: config.hubUsername, fromJupyterHub: true };
      }

      // Some deployments might use a different property
      if (config.user) {
        // Found username in page config
        return { username: config.user, fromJupyterHub: true };
      }
    }
  } catch (error) {
    console.error('Error parsing JupyterHub config:', error);
  }

  // Method 3: Try to extract from document.baseURI
  // Sometimes the base URI contains the username
  try {
    const baseUri = document.baseURI;
    const baseMatch = baseUri.match(/\/user\/([^\/]+)\//);

    if (baseMatch && baseMatch[1]) {
      // Make sure to decode the username to handle special characters like @ in email addresses
      const decodedUsername = decodeURIComponent(baseMatch[1]);
      // Found username from baseURI
      return { username: decodedUsername, fromJupyterHub: true };
    }
  } catch (error) {
    console.error('Error checking baseURI:', error);
  }

  // Method 4: Check cookies for JupyterHub-related information
  try {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
      const [name, value] = cookie.trim().split('=');
      if (name === 'jupyterhub-user') {
        // Found username in cookies
        return { username: decodeURIComponent(value), fromJupyterHub: true };
      }
    }
  } catch (error) {
    console.error('Error checking cookies:', error);
  }

  // Try a different regex pattern that might better handle complex usernames
  // This pattern is more permissive and might catch usernames with special characters
  const altRegex = /user\/([^\/]+)/;

  // Try with pathname first
  const altMatch = window.location.pathname.match(altRegex);
  if (altMatch && altMatch[1]) {
    const decodedUsername = decodeURIComponent(altMatch[1]);
    // Found username from alternative pattern
    return { username: decodedUsername, fromJupyterHub: true };
  }

  // Then try with full URL
  const altFullMatch = window.location.href.match(altRegex);
  if (altFullMatch && altFullMatch[1]) {
    const decodedUsername = decodeURIComponent(altFullMatch[1]);
    // Found username from alternative pattern in URL
    return { username: decodedUsername, fromJupyterHub: true };
  }

  // Try one more pattern specifically for email addresses in URLs
  const emailRegex = /user\/([^\/]+@[^\/]+)/;
  const emailMatch = window.location.href.match(emailRegex);
  if (emailMatch && emailMatch[1]) {
    const decodedUsername = decodeURIComponent(emailMatch[1]);
    // Found username with email pattern
    return { username: decodedUsername, fromJupyterHub: true };
  }

  // Not in a JupyterHub environment or username not found, return default username
  // No JupyterHub username found, using default
  return { username: "VoittaDefaultUser", fromJupyterHub: false };
}

/**
 * Default settings
 */
const DEFAULT_SETTINGS: IChatSettings = {
  maxMessages: 100,
  serverUrl: process.env.SERVER_URL || 'wss://hubserver.voitta.ai/ws',
  voittaApiKey: 'The Future Of Computing',
  openaiApiKey: '',
  anthropicApiKey: '',
  username: 'User',
  usernameFromJupyterHub: false,
  proxyPort: 3000
};

/**
 * A simple chat widget for Jupyter.
 */
export class ChatWidget extends Widget {
  private chatContainer: HTMLDivElement;
  private buttonContainer: HTMLDivElement;
  private divider: HTMLDivElement;
  private inputContainer: HTMLDivElement;
  private chatInput: HTMLTextAreaElement;
  private sendButton: HTMLButtonElement;
  private settings: IChatSettings = DEFAULT_SETTINGS;
  private stopIcon: HTMLDivElement;

  private voittaToolRouter: VoittaToolRouter | undefined;
  private messageHandler: MessageHandler;

  // Bound event handlers to ensure proper cleanup
  private boundDisableInput: EventListener;
  private boundEnableInput: EventListener;

  // Counter for generating unique IDs
  private static idCounter = 0;
  private app: JupyterFrontEnd;
  private notebookTracker: INotebookTracker;
  private settingsRegistry: ISettingRegistry | null;
  private debuggerService: IDebugger | null;

  private call_id_log = {};

  constructor(app: JupyterFrontEnd,
    settingsRegistry: ISettingRegistry | null,
    notebookTracker: INotebookTracker | null,
    debuggerService: IDebugger | null
  ) {
    // Generate a unique ID for this widget instance
    const id = `escobar-chat-${ChatWidget.idCounter++}`;
    super();

    this.app = app;
    this.notebookTracker = notebookTracker;
    this.settingsRegistry = settingsRegistry;
    this.debuggerService = debuggerService;
    this.id = id;
    this.addClass('escobar-chat');
    this.title.label = 'Voitta';
    this.title.caption = 'Escobar Voitta';
    this.title.iconClass = 'jp-MessageIcon'; // Add an icon for the sidebar
    this.title.closable = true;

    // Try to load settings from localStorage first
    try {
      const savedSettings = localStorage.getItem('escobar-settings');
      if (savedSettings) {
        const parsedSettings = JSON.parse(savedSettings);

        // Update settings with values from localStorage, using defaults for missing values
        this.settings = {
          maxMessages: parsedSettings.maxMessages || DEFAULT_SETTINGS.maxMessages,
          serverUrl: parsedSettings.serverUrl || DEFAULT_SETTINGS.serverUrl,
          voittaApiKey: parsedSettings.apiKey || parsedSettings.voittaApiKey || DEFAULT_SETTINGS.voittaApiKey,
          openaiApiKey: parsedSettings.openaiApiKey || DEFAULT_SETTINGS.openaiApiKey,
          anthropicApiKey: parsedSettings.anthropicApiKey || DEFAULT_SETTINGS.anthropicApiKey,
          username: parsedSettings.username || DEFAULT_SETTINGS.username,
          usernameFromJupyterHub: parsedSettings.usernameFromJupyterHub || DEFAULT_SETTINGS.usernameFromJupyterHub,
          proxyPort: parsedSettings.proxyPort || DEFAULT_SETTINGS.proxyPort
        };

        // Settings loaded from localStorage

        // Set the username as a global variable for the Python bridge
        (window as any).escobarUsername = this.settings.username;
      }
    } catch (error) {
      console.error('Failed to load settings from localStorage:', error);
    }

    // Create the main layout
    this.node.style.display = 'flex';
    this.node.style.flexDirection = 'column';
    this.node.style.height = '100%';
    this.node.style.padding = '5px';

    // Load settings if provided
    if (settingsRegistry) {
      this.loadSettings(settingsRegistry);
    }

    // Make sure the parent container has position relative for proper absolute positioning
    this.node.style.position = 'relative';

    // Create top buttons using the function from ui_elements.ts
    this.buttonContainer = createTopButtons(
      this.app,
      this.settingsRegistry,
      () => this.settings, // Function to get the current settings
      this.createNewChat.bind(this),
      this.init.bind(this),
      this.updateSettings.bind(this)
    );

    // Add the button container to the DOM
    this.node.appendChild(this.buttonContainer);

    // Button container created and appended to DOM

    // Create chat container
    this.chatContainer = document.createElement('div');
    this.chatContainer.className = 'escobar-chat-container';
    // Set initial height to 80% of the container
    this.chatContainer.style.height = '80%';
    this.chatContainer.style.flex = 'none';
    this.node.appendChild(this.chatContainer);

    // Create divider
    this.divider = document.createElement('div');
    this.divider.className = 'escobar-divider';
    this.node.appendChild(this.divider);

    // Add drag functionality to divider
    this.setupDividerDrag();

    // Create input container
    this.inputContainer = document.createElement('div');
    this.inputContainer.className = 'escobar-input-container';
    this.node.appendChild(this.inputContainer);

    // Create chat input
    this.chatInput = document.createElement('textarea');
    this.chatInput.className = 'escobar-chat-input';
    this.chatInput.placeholder = 'Type your message here...';
    this.chatInput.rows = 2;
    this.chatInput.addEventListener('keydown', (event: KeyboardEvent) => {
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        this.sendMessage(this.sendButton.textContent);
      }
    });
    this.inputContainer.appendChild(this.chatInput);

    // Create stop icon (authentic traffic stop sign)
    this.stopIcon = document.createElement('div');
    this.stopIcon.className = 'escobar-stop-icon';
    this.stopIcon.innerHTML = `
      <svg viewBox="0 0 100 100" width="100" height="100">
        <!-- Octagonal stop sign shape with white border -->
        <polygon points="29,5 71,5 95,29 95,71 71,95 29,95 5,71 5,29" fill="#c0392b" />
        <polygon points="29,5 71,5 95,29 95,71 71,95 29,95 5,71 5,29" fill="none" stroke="white" stroke-width="1.5" />
        <!-- STOP text - highway style, positioned slightly higher -->
        <text x="50" y="53" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" text-anchor="middle" dominant-baseline="middle" fill="white" letter-spacing="1">STOP</text>
      </svg>
    `;
    this.stopIcon.style.display = 'none'; // Initially hidden
    this.stopIcon.addEventListener('click', () => {
      window.dispatchEvent(new CustomEvent(PYTHON_CALL_EVENTS.STOP));
    });
    this.inputContainer.appendChild(this.stopIcon);

    // Create bound event handlers for proper cleanup
    this.boundDisableInput = this.disableInput.bind(this);
    this.boundEnableInput = this.enableInput.bind(this);

    // Add event listeners for Python call events to disable/enable the input area
    window.addEventListener(PYTHON_CALL_EVENTS.START, this.boundDisableInput);
    window.addEventListener(PYTHON_CALL_EVENTS.END, this.boundEnableInput);

    const splitButton: HTMLDivElement = createEscobarSplitButton(["Talk", "Plan", "Act"]);
    this.sendButton = splitButton["mainButton"];
    this.inputContainer.appendChild(splitButton);

    this.sendButton.addEventListener('click', () => {
      this.sendMessage(this.sendButton.textContent);
    });

    // Initialize the message handler
    this.messageHandler = new MessageHandler(
      this.settings.voittaApiKey,
      this.settings.openaiApiKey,
      this.settings.anthropicApiKey,
      this.settings.username,
      this.chatContainer,
      this.settings.maxMessages
    );

    setTimeout(async () => {
      await this.init();
    }, 1000);
  }

  private handlePythonResponse(response: any, responseMsg?: ResponseMessage): void {
    this.messageHandler.handlePythonResponse(response, responseMsg);
  }

  async say(args: any) {
    const msg = this.messageHandler.findMessageById(args["msg_call_id"]);
    if (msg.isNew) {
      msg.setContent(args["text"]);
      msg.isNew = false;
    } else {
      msg.setContent(msg.getContent() + args["text"]);
    }
  }

  async tool_say(args: any) {
    if ((typeof args["name"] != "string") || (typeof args["name"] == undefined)) {
      console.log(args);
      return;
    }

    if (voittal_call_log[args.id] != undefined) {
      // Streaming finished call
    }

    if (args["name"].includes("editExecuteCell_editExecuteCell") ||
      args["name"].includes("insertExecuteCell_insertExecuteCell") ||
      args["name"].includes("writeToFile_writeToFile") ||
      args["name"].includes("diffToFile_diffToFile")
    ) {
      try {
        if (this.call_id_log[args.id] == undefined) {
          this.call_id_log[args.id] = "";
        }
        this.call_id_log[args.id] += args.text;

        var parsed = {};

        try {
          parsed = JSON.parse(this.call_id_log[args.id]);
        } catch {
          parsed = JSON.parse(this.call_id_log[args.id] + '"}');
        }

        if (args["name"].includes("diffToFile_diffToFile")) {
          const search = parsed["search"];
          const replace = parsed["replace"];
          const filePath = parsed["filePath"];
          if ((search != undefined) && (replace != undefined)) {
            const funcion_name = args["name"].split("_").reverse()[1];
            const callResult = await functions[funcion_name].func(
              {
                "filePath": filePath, "search": search, "replace": replace
              }, true, args.id
            )
          }
        } else if (args["name"].includes("writeToFile_writeToFile")) {
          const content = parsed["content"];
          const filePath = parsed["filePath"];
          if (content) {
            const funcion_name = args["name"].split("_").reverse()[1];
            const callResult = await functions[funcion_name].func(
              {
                "filePath": filePath, "content": content
              }, true, args.id
            )
          }
        } else {
          const content = parsed["content"];
          const cellType = parsed["cellType"];
          const index = parseInt(parsed["index"], 10);
          if (content) {
            const funcion_name = args["name"].split("_").reverse()[1]; // this is super voitta-specific....
            const callResult = await functions[funcion_name].func({
              "index": index,
              "cellType": cellType,
              "content": content
            }, true, args.id);
          }
        }


      } catch (error) {
        //console.error('Failed to repair/parse JSON:', error);
      }
    }
  }

  async init() {
    await this.messageHandler.clearMessages();
    this.voittaToolRouter = new VoittaToolRouter();
    const tools = await get_tools(this.app, this.notebookTracker, this.debuggerService);

    // First check if we're in JupyterHub mode
    const isJupyterHub = window.location.href.includes('/user/');

    if (isJupyterHub) {
      // In JupyterHub mode, ALWAYS get the username from the URL
      // Get JupyterHub username from URL
      const usernameInfo = getJupyterHubUsername();

      // Force update the username in JupyterHub mode
      if (usernameInfo.fromJupyterHub) {
        this.settings.username = usernameInfo.username;
        this.settings.usernameFromJupyterHub = true;
        // Using username from JupyterHub URL
      }
    } else if (!this.settings.username || this.settings.usernameFromJupyterHub) {
      // Not in JupyterHub mode, but we need to update the username
      // Get username or default
      const usernameInfo = getJupyterHubUsername();

      // Update if needed
      if (usernameInfo.fromJupyterHub || !this.settings.username) {
        this.settings.username = usernameInfo.username;
        this.settings.usernameFromJupyterHub = usernameInfo.fromJupyterHub;
        // Username updated
      }
    } else {
      // Using saved username (custom user-defined)
    }

    // Update global variable
    (window as any).escobarUsername = this.settings.username;

    // Save to localStorage
    try {
      localStorage.setItem('escobar-settings', JSON.stringify(this.settings));
      // Settings saved to localStorage
    } catch (error) {
      console.error('Failed to save settings to localStorage:', error);
    }

    registerFunction('handleResponse', false, this.handlePythonResponse.bind(this));
    registerFunction('say', false, this.say.bind(this));
    registerFunction('tool_say', false, this.tool_say.bind(this));

    this.voittaToolRouter.tools = tools;

    try {
      // Use serverUrl from settings
      await initPythonBridge(this.settings.serverUrl);
      // WebSocket connected successfully
    } catch (e) {
      console.error(e);
    }

    await this.messageHandler.loadMessages();

    // this is a very stupid approach....
    let start_call_id = this.messageHandler.generateMessageId();
    const payload = JSON.stringify({
      method: "start",
      message_type: "request",
      api_key: this.settings.voittaApiKey,
      openai_api_key: this.settings.openaiApiKey,
      anthropic_api_key: this.settings.anthropicApiKey,
      call_id: start_call_id,
      intraspection: this.voittaToolRouter.intraspect(),
      rootPath: "rootPath"
    });

    const response = await callPython(payload);
  }

  /**
   * Load settings from the settings registry
   */
  private loadSettings(settingsRegistry: ISettingRegistry): void {
    settingsRegistry
      .load('escobar:plugin')
      .then(settings => {
        // Get the settings from the registry
        const loadedSettings = settings.composite as any as IChatSettings;

        // Update settings
        this.updateSettings(loadedSettings);

        // Listen for setting changes
        settings.changed.connect(() => {
          // Settings changed in registry
          const updatedSettings = settings.composite as any as IChatSettings;
          this.updateSettings(updatedSettings);
        });
      })
      .catch(reason => {
        console.error('Failed to load settings for escobar.', reason);
      });
  }

  /**
   * Update settings
   */
  private updateSettings(settings: IChatSettings): void {
    // Store the previous server URL to check if it changed
    const previousServerUrl = this.settings.serverUrl;

    // Update settings with new values
    this.settings = {
      maxMessages: settings.maxMessages || DEFAULT_SETTINGS.maxMessages,
      serverUrl: settings.serverUrl || DEFAULT_SETTINGS.serverUrl,
      voittaApiKey: settings.voittaApiKey || DEFAULT_SETTINGS.voittaApiKey,
      openaiApiKey: settings.openaiApiKey || DEFAULT_SETTINGS.openaiApiKey,
      anthropicApiKey: settings.anthropicApiKey || DEFAULT_SETTINGS.anthropicApiKey,
      username: settings.username || DEFAULT_SETTINGS.username,
      usernameFromJupyterHub: settings.usernameFromJupyterHub || DEFAULT_SETTINGS.usernameFromJupyterHub,
      proxyPort: settings.proxyPort || DEFAULT_SETTINGS.proxyPort
    };

    // Update message handler settings
    this.messageHandler.updateSettings(
      this.settings.voittaApiKey,
      this.settings.openaiApiKey,
      this.settings.anthropicApiKey,
      this.settings.username,
      this.settings.maxMessages
    );

    // Set the username as a global variable for the Python bridge
    (window as any).escobarUsername = this.settings.username;
    // Global username updated

    // Save settings to localStorage for persistence across page reloads
    try {
      localStorage.setItem('escobar-settings', JSON.stringify(this.settings));
      // Settings saved to localStorage
    } catch (error) {
      console.error('Failed to save settings to localStorage:', error);
    }

    // Apply settings to UI components if needed
    this.applySettingsToUI();

    // Check if the server URL has changed
    if (previousServerUrl !== this.settings.serverUrl) {
      // Server URL changed

      // Close the existing WebSocket connection
      const ws = get_ws();
      if (ws) {
        // Closing existing WebSocket connection
        ws.close();
      }

      // Reinitialize with the new URL
      setTimeout(() => {
        this.init();
      }, 100); // Small delay to ensure the previous connection is fully closed
    }
  }

  /**
   * Apply settings to UI components
   */
  private applySettingsToUI(): void {
    // Applying settings to UI components

    // If there are any UI components that need to be updated based on settings,
    // update them here. For example, if there's a display of the current username,
    // update it with this.settings.username.

    // This method can be extended as more UI components are added that depend on settings.
  }

  /**
   * Disable the input area during Python calls
   */
  private disableInput(): void {
    if (this.chatInput) {
      this.chatInput.disabled = true;
      this.chatInput.style.opacity = '0.6';
      this.chatInput.placeholder = 'Processing...';

      // Show the stop icon
      if (this.stopIcon) {
        this.stopIcon.style.display = 'flex';
      }
    }
  }

  /**
   * Enable the input area after Python calls complete
   */
  private enableInput(): void {
    if (this.chatInput) {
      this.chatInput.disabled = false;
      this.chatInput.style.opacity = '1';
      this.chatInput.placeholder = 'Type your message here...';

      // Hide the stop icon
      if (this.stopIcon) {
        this.stopIcon.style.display = 'none';
      }
    }
  }

  private async createNewChat(): Promise<void> {
    await this.messageHandler.createNewChat();
    this.init();
  }

  /**
   * Send a message from the input field.
   */
  private async sendMessage(mode: string): Promise<void> {
    const content = this.chatInput.value.trim();

    if (!content) {
      return;
    }

    // Clear input
    this.chatInput.value = '';

    // Send message using the message handler
    await this.messageHandler.sendMessage(content, mode);
  }

  /**
   * Handle activation requests for the widget
   */
  protected onActivateRequest(msg: Message): void {
    super.onActivateRequest(msg);
    this.chatInput.focus();
  }

  /**
   * Setup drag functionality for the divider
   */
  private setupDividerDrag(): void {
    let isDragging = false;
    let startY = 0;
    let startHeight = 0;

    const isScrolledToBottom = () => {
      // Get the scroll position
      const scrollTop = this.chatContainer.scrollTop;
      // Get the visible height
      const clientHeight = this.chatContainer.clientHeight;
      // Get the total scrollable height
      const scrollHeight = this.chatContainer.scrollHeight;

      // If scrollTop + clientHeight is approximately equal to scrollHeight,
      // then the container is scrolled to the bottom
      // (using a small threshold to account for rounding errors)

      return Math.abs(scrollTop + clientHeight - scrollHeight) < 100;
    };

    // Mouse move event handler
    const onMouseMove = (e: MouseEvent) => {
      if (!isDragging) return;

      // Calculate exact delta from start position
      const delta = e.pageY - startY - 18;

      // Get container height to calculate minimum and maximum allowed height
      const containerHeight = this.node.offsetHeight;
      const minChatHeight = Math.max(100, containerHeight * 0.3); // At least 30% of container or 100px
      const maxChatHeight = containerHeight * 0.85; // At most 85% of container

      // Apply delta directly to the starting height with min/max constraints
      const newHeight = Math.min(maxChatHeight, Math.max(minChatHeight, startHeight + delta));

      // Update chat container height
      this.chatContainer.style.height = `${newHeight}px`;
      this.chatContainer.style.flex = 'none';

      if (isScrolledToBottom()) {
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
      }
    };

    // Mouse up event handler
    const onMouseUp = () => {
      if (!isDragging) return;

      isDragging = false;

      // Remove temporary event listeners
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);

      // Restore text selection
      document.body.style.userSelect = '';
    };

    // Attach mousedown event to divider
    this.divider.addEventListener('mousedown', (e: MouseEvent) => {
      // Prevent default to avoid text selection
      e.preventDefault();
      e.stopPropagation();

      // Store initial values
      isDragging = true;
      startY = e.pageY;
      startHeight = this.chatContainer.offsetHeight;

      // Add temporary event listeners
      window.addEventListener('mousemove', onMouseMove);
      window.addEventListener('mouseup', onMouseUp);

      // Prevent text selection during drag
      document.body.style.userSelect = 'none';
    });
  }

  /**
   * Dispose of the widget and clean up resources
   */
  dispose(): void {
    // Remove event listeners
    window.removeEventListener(PYTHON_CALL_EVENTS.START, this.boundDisableInput);
    window.removeEventListener(PYTHON_CALL_EVENTS.END, this.boundEnableInput);

    // Close WebSocket connection when widget is disposed
    const ws = get_ws();
    if (ws) {
      ws.close();
    }
    super.dispose();
  }
}
