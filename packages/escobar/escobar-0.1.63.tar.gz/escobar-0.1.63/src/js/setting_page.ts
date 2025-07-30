import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { showLoginUI } from '../utils/loginUI';
import { VERSION } from '../version';

/**
 * Interface for chat settings
 */
export interface IChatSettings {
  maxMessages: number;
  serverUrl: string;
  voittaApiKey: string;  // Renamed from apiKey
  openaiApiKey: string;  // New property
  anthropicApiKey: string;  // New property
  username: string;
  usernameFromJupyterHub: boolean;
  proxyPort?: number;
}

/**
 * Determines if the current environment is JupyterHub based on URL pattern
 * @returns True if running in JupyterHub environment, false otherwise
 */
export function isJupyterHubEnvironment(): boolean {
  // Check URL pattern - most reliable in JupyterHub
  // JupyterHub URLs typically follow the pattern: /user/{username}/lab/...
  const hubUserRegex = /\/user\/([^\/]+)\//;
  const hubUserMatch = window.location.pathname.match(hubUserRegex);

  if (hubUserMatch && hubUserMatch[1]) {
    return true;
  }

  // Check for JupyterHub data in the page config
  try {
    const configElement = document.getElementById('jupyter-config-data');
    if (configElement && configElement.textContent) {
      const config = JSON.parse(configElement.textContent);

      if (config.hubUser || config.hubUsername || config.user) {
        return true;
      }
    }
  } catch (error) {
    console.error('Error parsing JupyterHub config:', error);
  }

  // Try to extract from document.baseURI
  try {
    const baseUri = document.baseURI;
    const baseMatch = baseUri.match(/\/user\/([^\/]+)\//);

    if (baseMatch && baseMatch[1]) {
      return true;
    }
  } catch (error) {
    console.error('Error checking baseURI:', error);
  }

  // Check cookies for JupyterHub-related information
  try {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
      const [name, value] = cookie.trim().split('=');
      if (name === 'jupyterhub-user') {
        return true;
      }
    }
  } catch (error) {
    console.error('Error checking cookies:', error);
  }

  // Try a different regex pattern that might better handle complex usernames
  const altRegex = /\/user\/([^\/]*)\//;
  const altMatch = window.location.pathname.match(altRegex);

  if (altMatch && altMatch[1]) {
    return true;
  }

  return false;
}

/**
 * Factory function to create the appropriate settings page based on environment
 * @param settingsRegistry The settings registry
 * @param currentSettings The current settings
 * @param onSave Callback function when settings are saved
 * @returns The appropriate settings page instance
 */
export function createSettingsPage(
  settingsRegistry: ISettingRegistry,
  currentSettings: IChatSettings,
  onSave: (settings: IChatSettings) => void
): BaseSettingsPage {
  const isJupyterHub = isJupyterHubEnvironment();

  if (isJupyterHub) {
    return new JupyterHubSettingsPage(settingsRegistry, currentSettings, onSave);
  } else {
    return new PluginSettingsPage(settingsRegistry, currentSettings, onSave);
  }
}

/**
 * Abstract base class for settings pages
 */
export abstract class BaseSettingsPage {
  protected settingsRegistry: ISettingRegistry;
  protected container: HTMLDivElement;
  protected overlay: HTMLDivElement;
  protected currentSettings: IChatSettings;
  protected onSave: (settings: IChatSettings) => void;

  /**
   * Create a new SettingsPage
   * @param settingsRegistry The settings registry
   * @param currentSettings The current settings
   * @param onSave Callback function when settings are saved
   */
  constructor(
    settingsRegistry: ISettingRegistry,
    currentSettings: IChatSettings,
    onSave: (settings: IChatSettings) => void
  ) {
    this.settingsRegistry = settingsRegistry;
    this.currentSettings = currentSettings;
    this.onSave = onSave;

    // Create overlay
    this.overlay = document.createElement('div');
    this.overlay.className = 'escobar-settings-overlay';
    this.overlay.addEventListener('click', (e) => {
      if (e.target === this.overlay) {
        this.hide();
      }
    });

    // Create container
    this.container = this.createContainer();
    this.overlay.appendChild(this.container);
  }

  /**
   * Create the settings UI container
   * This is an abstract method that must be implemented by derived classes
   */
  protected abstract createContainer(): HTMLDivElement;

  /**
   * Create a standard header for the settings container
   * @param title The title to display in the header
   * @returns The created header element
   */
  protected createHeader(title: string): HTMLDivElement {
    const header = document.createElement('div');
    header.className = 'escobar-settings-header';

    const titleElement = document.createElement('h2');
    titleElement.textContent = title;
    header.appendChild(titleElement);

    const closeButton = document.createElement('button');
    closeButton.className = 'escobar-settings-close-button';
    closeButton.innerHTML = '&times;';
    closeButton.addEventListener('click', () => this.hide());
    header.appendChild(closeButton);

    return header;
  }

  /**
   * Create a form group with label and description
   * @param id The ID for the input element
   * @param labelText The text for the label
   * @param descriptionText The description text
   * @returns The created form group element
   */
  protected createFormGroup(id: string, labelText: string, descriptionText: string): HTMLDivElement {
    const group = document.createElement('div');
    group.className = 'escobar-settings-group';

    const label = document.createElement('label');
    label.textContent = labelText;
    label.htmlFor = id;
    group.appendChild(label);

    const description = document.createElement('div');
    description.className = 'escobar-settings-description';
    description.textContent = descriptionText;
    group.appendChild(description);

    return group;
  }

  /**
   * Create a standard buttons container with Save and Cancel buttons
   * @returns The created buttons container
   */
  protected createButtonsContainer(): HTMLDivElement {
    const buttonsContainer = document.createElement('div');
    buttonsContainer.className = 'escobar-settings-buttons';

    const cancelButton = document.createElement('button');
    cancelButton.className = 'escobar-settings-button escobar-settings-cancel-button';
    cancelButton.textContent = 'Cancel';
    cancelButton.type = 'button';
    cancelButton.addEventListener('click', () => this.hide());
    buttonsContainer.appendChild(cancelButton);

    const saveButton = document.createElement('button');
    saveButton.className = 'escobar-settings-button escobar-settings-save-button';
    saveButton.textContent = 'Save';
    saveButton.type = 'submit';
    buttonsContainer.appendChild(saveButton);

    return buttonsContainer;
  }

  /**
   * Show the settings page
   */
  public show(): void {
    // Fetch the latest settings from the registry before showing the form
    this.settingsRegistry.load('escobar:plugin')
      .then(settings => {
        // Update current settings with the latest from the registry
        const latestSettings = settings.composite as any as IChatSettings;

        // Merge with default settings to ensure all fields are present
        this.currentSettings = {
          maxMessages: latestSettings.maxMessages || this.currentSettings.maxMessages,
          serverUrl: latestSettings.serverUrl || this.currentSettings.serverUrl,
          voittaApiKey: latestSettings.voittaApiKey || this.currentSettings.voittaApiKey,
          openaiApiKey: latestSettings.openaiApiKey || this.currentSettings.openaiApiKey,
          anthropicApiKey: latestSettings.anthropicApiKey || this.currentSettings.anthropicApiKey,
          username: latestSettings.username || this.currentSettings.username,
          usernameFromJupyterHub: latestSettings.usernameFromJupyterHub || this.currentSettings.usernameFromJupyterHub,
          proxyPort: latestSettings.proxyPort || this.currentSettings.proxyPort || 3000
        };

        // Update form fields with the latest settings
        this.updateFormFields();

        // Show the settings page
        document.body.appendChild(this.overlay);
        // Add animation class after a small delay to trigger animation
        setTimeout(() => {
          this.overlay.classList.add('escobar-settings-overlay-visible');
          this.container.classList.add('escobar-settings-container-visible');
        }, 10);
      })
      .catch(error => {
        console.error('Failed to load latest settings from registry:', error);

        // Fall back to using the current settings
        this.updateFormFields();

        // Show the settings page anyway
        document.body.appendChild(this.overlay);
        // Add animation class after a small delay to trigger animation
        setTimeout(() => {
          this.overlay.classList.add('escobar-settings-overlay-visible');
          this.container.classList.add('escobar-settings-container-visible');
        }, 10);
      });

    const proxyPortInput = document.getElementById('escobar-proxy-port') as HTMLInputElement;
    if (proxyPortInput) proxyPortInput.value = (this.currentSettings.proxyPort || 3000).toString();
  }

  /**
   * Update form fields with current settings
   * This method should be implemented by derived classes to update their specific form fields
   */
  protected abstract updateFormFields(): void;

  /**
   * Hide the settings page
   */
  public hide(): void {
    this.overlay.classList.remove('escobar-settings-overlay-visible');
    this.container.classList.remove('escobar-settings-container-visible');

    // Remove from DOM after animation completes
    setTimeout(() => {
      if (this.overlay.parentNode) {
        this.overlay.parentNode.removeChild(this.overlay);
      }
    }, 300); // Match the CSS transition duration
  }

  /**
   * Save settings changes
   * This method should be implemented by derived classes to handle their specific form fields
   */
  protected abstract saveSettings(): void;

  /**
   * Validate and save common settings
   * @param formValues The form values to validate and save
   * @returns True if validation passed, false otherwise
   */
  protected validateAndSaveCommonSettings(formValues: {
    maxMessages: number,
    serverUrl: string,
    voittaApiKey: string,
    openaiApiKey: string,
    anthropicApiKey: string,
    username: string,
    proxyPort?: number
  }): boolean {
    // Validate input
    if (isNaN(formValues.maxMessages) || formValues.maxMessages < 10 || formValues.maxMessages > 1000) {
      alert('Maximum Messages must be a number between 10 and 1000');
      return false;
    }

    if (!formValues.serverUrl) {
      alert('Server URL is required');
      return false;
    }

    // At least one API key is required
    if (!formValues.voittaApiKey && !formValues.openaiApiKey && !formValues.anthropicApiKey) {
      alert('At least one API Key is required');
      return false;
    }

    if (!formValues.username) {
      alert('Username is required');
      return false;
    }

    // Create new settings object
    const newSettings: IChatSettings = {
      maxMessages: formValues.maxMessages,
      serverUrl: formValues.serverUrl,
      voittaApiKey: formValues.voittaApiKey,
      openaiApiKey: formValues.openaiApiKey,
      anthropicApiKey: formValues.anthropicApiKey,
      username: formValues.username,
      // Preserve the usernameFromJupyterHub value from current settings
      usernameFromJupyterHub: this.currentSettings.usernameFromJupyterHub,
      proxyPort: formValues.proxyPort || 3000
    };

    // First update the current settings to ensure they're immediately available
    this.currentSettings = newSettings;

    // Call onSave callback before hiding the settings page
    // This ensures the settings are applied immediately
    this.onSave(newSettings);

    // Save settings to registry
    this.settingsRegistry.load('escobar:plugin')
      .then(settings => {
        settings.set('maxMessages', formValues.maxMessages);
        settings.set('serverUrl', formValues.serverUrl);
        settings.set('voittaApiKey', formValues.voittaApiKey);
        settings.set('openaiApiKey', formValues.openaiApiKey);
        settings.set('anthropicApiKey', formValues.anthropicApiKey);
        settings.set('username', formValues.username);
        settings.set('usernameFromJupyterHub', newSettings.usernameFromJupyterHub);
        settings.set('proxyPort', newSettings.proxyPort);

        // Hide settings page
        this.hide();
      })
      .catch(reason => {
        console.error('Failed to save settings for escobar.', reason);
        alert('Failed to save settings. Please try again.');
      });

    return true;
  }
}

/**
 * JupyterHub-specific settings page implementation
 */
export class JupyterHubSettingsPage extends BaseSettingsPage {
  /**
   * Create the settings UI container for JupyterHub environment
   */
  protected createContainer(): HTMLDivElement {
    // Create container
    const container = document.createElement('div');
    container.className = 'escobar-settings-container';

    // Create header with JupyterHub-specific title
    const header = this.createHeader('JupyterHub Settings');
    container.appendChild(header);

    // Add mode indicator label with version number
    const modeIndicator = document.createElement('div');
    modeIndicator.className = 'escobar-mode-indicator';
    modeIndicator.innerHTML = `Running in JupyterHub Mode <span style="font-size: 0.8em; opacity: 0.8;">v${VERSION}</span>`;
    modeIndicator.style.backgroundColor = '#f0f7ff';
    modeIndicator.style.color = '#0366d6';
    modeIndicator.style.padding = '8px 16px';
    modeIndicator.style.margin = '0 16px 16px 16px';
    modeIndicator.style.borderRadius = '4px';
    modeIndicator.style.fontWeight = 'bold';
    modeIndicator.style.textAlign = 'center';
    modeIndicator.style.border = '1px solid #c8e1ff';
    container.appendChild(modeIndicator);

    // Create form
    const form = document.createElement('form');
    form.className = 'escobar-settings-form';
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      this.saveSettings();
    });

    // Create form fields

    // Max messages field
    const maxMessagesGroup = this.createFormGroup(
      'escobar-max-messages',
      'Maximum Messages',
      'The maximum number of messages to keep in the chat history.'
    );

    const maxMessagesInput = document.createElement('input');
    maxMessagesInput.id = 'escobar-max-messages';
    maxMessagesInput.className = 'escobar-settings-input';
    maxMessagesInput.type = 'number';
    maxMessagesInput.min = '10';
    maxMessagesInput.max = '1000';
    maxMessagesInput.value = this.currentSettings.maxMessages.toString();
    maxMessagesGroup.appendChild(maxMessagesInput);

    form.appendChild(maxMessagesGroup);

    // Server URL field
    const serverUrlGroup = this.createFormGroup(
      'escobar-server-url',
      'Voitta AI Server',
      'The URL of the WebSocket server to connect to.'
    );

    const serverUrlInput = document.createElement('input');
    serverUrlInput.id = 'escobar-server-url';
    serverUrlInput.className = 'escobar-settings-input';
    serverUrlInput.type = 'text';
    serverUrlInput.value = this.currentSettings.serverUrl;
    serverUrlGroup.appendChild(serverUrlInput);

    form.appendChild(serverUrlGroup);

    // Voitta API Key field
    const voittaApiKeyGroup = this.createFormGroup(
      'escobar-voitta-api-key',
      'Voitta API Key',
      'The API key for authentication with Voitta services. (Optional)'
    );

    const voittaApiKeyInput = document.createElement('input');
    voittaApiKeyInput.id = 'escobar-voitta-api-key';
    voittaApiKeyInput.className = 'escobar-settings-input';
    voittaApiKeyInput.type = 'text';
    voittaApiKeyInput.value = this.currentSettings.voittaApiKey || '';
    voittaApiKeyGroup.appendChild(voittaApiKeyInput);

    // Add "Get API Key" link for Voitta
    const getVoittaApiKeyLink = document.createElement('a');
    getVoittaApiKeyLink.href = '#';
    getVoittaApiKeyLink.className = 'escobar-get-api-key-link';
    getVoittaApiKeyLink.textContent = 'Get Voitta API Key';
    getVoittaApiKeyLink.style.display = this.currentSettings.voittaApiKey ? 'none' : 'block';
    getVoittaApiKeyLink.addEventListener('click', (e) => {
      e.preventDefault();

      // Show the login UI
      showLoginUI()
        .then((apiKey) => {
          // Update the API key input
          voittaApiKeyInput.value = apiKey;

          // Hide the link
          getVoittaApiKeyLink.style.display = 'none';

          // Show success message
          alert('Successfully obtained Voitta API key!');
        })
        .catch((error) => {
          if (error.message !== 'Authentication cancelled') {
            console.error('Authentication error:', error);
            alert('Failed to authenticate. Please try again.');
          }
        });
    });
    voittaApiKeyGroup.appendChild(getVoittaApiKeyLink);

    // Add event listener to show/hide the link based on input value
    voittaApiKeyInput.addEventListener('input', () => {
      getVoittaApiKeyLink.style.display = voittaApiKeyInput.value ? 'none' : 'block';
    });

    form.appendChild(voittaApiKeyGroup);

    // OpenAI API Key field
    const openaiApiKeyGroup = this.createFormGroup(
      'escobar-openai-api-key',
      'OpenAI API Key',
      'Your OpenAI API key for OpenAI-powered features. (Optional)'
    );

    const openaiApiKeyInput = document.createElement('input');
    openaiApiKeyInput.id = 'escobar-openai-api-key';
    openaiApiKeyInput.className = 'escobar-settings-input';
    openaiApiKeyInput.type = 'text';
    openaiApiKeyInput.value = this.currentSettings.openaiApiKey || '';
    openaiApiKeyGroup.appendChild(openaiApiKeyInput);

    form.appendChild(openaiApiKeyGroup);

    // Anthropic API Key field
    const anthropicApiKeyGroup = this.createFormGroup(
      'escobar-anthropic-api-key',
      'Anthropic API Key',
      'Your Anthropic API key for Claude-powered features. (Optional)'
    );

    const anthropicApiKeyInput = document.createElement('input');
    anthropicApiKeyInput.id = 'escobar-anthropic-api-key';
    anthropicApiKeyInput.className = 'escobar-settings-input';
    anthropicApiKeyInput.type = 'text';
    anthropicApiKeyInput.value = this.currentSettings.anthropicApiKey || '';
    anthropicApiKeyGroup.appendChild(anthropicApiKeyInput);

    form.appendChild(anthropicApiKeyGroup);

    // Username field - always disabled in JupyterHub environment
    const usernameGroup = this.createFormGroup(
      'escobar-username',
      'Username',
      'Your display name for chat messages.'
    );

    const usernameInput = document.createElement('input');
    usernameInput.id = 'escobar-username';
    usernameInput.className = 'escobar-settings-input';
    usernameInput.type = 'text';
    usernameInput.value = this.currentSettings.username;
    usernameInput.disabled = true;
    usernameInput.style.opacity = '0.7';
    usernameInput.style.cursor = 'not-allowed';

    // Add a note explaining the username source and why it's disabled
    const jupyterHubNote = document.createElement('div');
    jupyterHubNote.className = 'escobar-settings-note';
    jupyterHubNote.style.fontSize = '0.85em';
    jupyterHubNote.style.fontStyle = 'italic';
    jupyterHubNote.style.marginTop = '5px';
    jupyterHubNote.style.color = '#666';
    jupyterHubNote.textContent = `Username is extracted from your JupyterHub URL and cannot be changed.`;
    usernameGroup.appendChild(jupyterHubNote);

    usernameGroup.appendChild(usernameInput);
    form.appendChild(usernameGroup);

    // Proxy Port field
    const proxyPortGroup = this.createFormGroup(
      'escobar-proxy-port',
      'Proxy Port',
      'The port number for the proxy server.'
    );

    const proxyPortInput = document.createElement('input');
    proxyPortInput.id = 'escobar-proxy-port';
    proxyPortInput.className = 'escobar-settings-input';
    proxyPortInput.type = 'number';
    proxyPortInput.min = '1';
    proxyPortInput.max = '65535';
    proxyPortInput.value = (this.currentSettings.proxyPort || 3000).toString();
    proxyPortGroup.appendChild(proxyPortInput);

    form.appendChild(proxyPortGroup);

    // Create buttons
    const buttonsContainer = this.createButtonsContainer();
    form.appendChild(buttonsContainer);

    container.appendChild(form);

    return container;
  }

  /**
   * Update form fields with current settings
   */
  protected updateFormFields(): void {
    // Get form elements
    const maxMessagesInput = document.getElementById('escobar-max-messages') as HTMLInputElement;
    const serverUrlInput = document.getElementById('escobar-server-url') as HTMLInputElement;
    const voittaApiKeyInput = document.getElementById('escobar-voitta-api-key') as HTMLInputElement;
    const openaiApiKeyInput = document.getElementById('escobar-openai-api-key') as HTMLInputElement;
    const anthropicApiKeyInput = document.getElementById('escobar-anthropic-api-key') as HTMLInputElement;
    const usernameInput = document.getElementById('escobar-username') as HTMLInputElement;
    const proxyPortInput = document.getElementById('escobar-proxy-port') as HTMLInputElement;

    // Update values with current settings
    if (maxMessagesInput) maxMessagesInput.value = this.currentSettings.maxMessages.toString();
    if (serverUrlInput) serverUrlInput.value = this.currentSettings.serverUrl;
    if (voittaApiKeyInput) voittaApiKeyInput.value = this.currentSettings.voittaApiKey || '';
    if (openaiApiKeyInput) openaiApiKeyInput.value = this.currentSettings.openaiApiKey || '';
    if (anthropicApiKeyInput) anthropicApiKeyInput.value = this.currentSettings.anthropicApiKey || '';
    if (usernameInput) usernameInput.value = this.currentSettings.username;
    if (proxyPortInput) proxyPortInput.value = (this.currentSettings.proxyPort || 3000).toString();
  }

  /**
   * Save settings changes
   */
  protected saveSettings(): void {
    // Get values from form
    const maxMessagesInput = document.getElementById('escobar-max-messages') as HTMLInputElement;
    const serverUrlInput = document.getElementById('escobar-server-url') as HTMLInputElement;
    const voittaApiKeyInput = document.getElementById('escobar-voitta-api-key') as HTMLInputElement;
    const openaiApiKeyInput = document.getElementById('escobar-openai-api-key') as HTMLInputElement;
    const anthropicApiKeyInput = document.getElementById('escobar-anthropic-api-key') as HTMLInputElement;
    const usernameInput = document.getElementById('escobar-username') as HTMLInputElement;
    const proxyPortInput = document.getElementById('escobar-proxy-port') as HTMLInputElement;

    // Validate and save settings
    this.validateAndSaveCommonSettings({
      maxMessages: parseInt(maxMessagesInput.value, 10),
      serverUrl: serverUrlInput.value.trim(),
      voittaApiKey: voittaApiKeyInput.value.trim(),
      openaiApiKey: openaiApiKeyInput.value.trim(),
      anthropicApiKey: anthropicApiKeyInput.value.trim(),
      username: usernameInput.value.trim(),
      proxyPort: proxyPortInput ? parseInt(proxyPortInput.value, 10) : 3000
    });
  }
}

/**
 * Plugin-specific settings page implementation
 */
export class PluginSettingsPage extends BaseSettingsPage {
  /**
   * Create the settings UI container for plugin environment
   */
  protected createContainer(): HTMLDivElement {
    // Create container
    const container = document.createElement('div');
    container.className = 'escobar-settings-container';

    // Create header with plugin-specific title
    const header = this.createHeader('Plugin Settings');
    container.appendChild(header);

    // Add mode indicator label with version number
    const modeIndicator = document.createElement('div');
    modeIndicator.className = 'escobar-mode-indicator';
    modeIndicator.innerHTML = `Running in Plugin Mode <span style="font-size: 0.8em; opacity: 0.8;">v${VERSION}</span>`;
    modeIndicator.style.backgroundColor = '#f6f8fa';
    modeIndicator.style.color = '#24292e';
    modeIndicator.style.padding = '8px 16px';
    modeIndicator.style.margin = '0 16px 16px 16px';
    modeIndicator.style.borderRadius = '4px';
    modeIndicator.style.fontWeight = 'bold';
    modeIndicator.style.textAlign = 'center';
    modeIndicator.style.border = '1px solid #e1e4e8';
    container.appendChild(modeIndicator);

    // Create form
    const form = document.createElement('form');
    form.className = 'escobar-settings-form';
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      this.saveSettings();
    });

    // Create form fields

    // Max messages field
    const maxMessagesGroup = this.createFormGroup(
      'escobar-max-messages',
      'Maximum Messages',
      'The maximum number of messages to keep in the chat history.'
    );

    const maxMessagesInput = document.createElement('input');
    maxMessagesInput.id = 'escobar-max-messages';
    maxMessagesInput.className = 'escobar-settings-input';
    maxMessagesInput.type = 'number';
    maxMessagesInput.min = '10';
    maxMessagesInput.max = '1000';
    maxMessagesInput.value = this.currentSettings.maxMessages.toString();
    maxMessagesGroup.appendChild(maxMessagesInput);

    form.appendChild(maxMessagesGroup);

    // Server URL field
    const serverUrlGroup = this.createFormGroup(
      'escobar-server-url',
      'Voitta AI Server',
      'The URL of the WebSocket server to connect to.'
    );

    const serverUrlInput = document.createElement('input');
    serverUrlInput.id = 'escobar-server-url';
    serverUrlInput.className = 'escobar-settings-input';
    serverUrlInput.type = 'text';
    serverUrlInput.value = this.currentSettings.serverUrl;
    serverUrlGroup.appendChild(serverUrlInput);

    form.appendChild(serverUrlGroup);

    // Voitta API Key field
    const voittaApiKeyGroup = this.createFormGroup(
      'escobar-voitta-api-key',
      'Voitta API Key',
      'The API key for authentication with Voitta services. (Optional)'
    );

    const voittaApiKeyInput = document.createElement('input');
    voittaApiKeyInput.id = 'escobar-voitta-api-key';
    voittaApiKeyInput.className = 'escobar-settings-input';
    voittaApiKeyInput.type = 'text';
    voittaApiKeyInput.value = this.currentSettings.voittaApiKey || '';
    voittaApiKeyGroup.appendChild(voittaApiKeyInput);

    // Add "Get API Key" link for Voitta
    const getVoittaApiKeyLink = document.createElement('a');
    getVoittaApiKeyLink.href = '#';
    getVoittaApiKeyLink.className = 'escobar-get-api-key-link';
    getVoittaApiKeyLink.textContent = 'Get Voitta API Key';
    getVoittaApiKeyLink.style.display = this.currentSettings.voittaApiKey ? 'none' : 'block';
    getVoittaApiKeyLink.addEventListener('click', (e) => {
      e.preventDefault();

      // Show the login UI
      showLoginUI()
        .then((apiKey) => {
          // Update the API key input
          voittaApiKeyInput.value = apiKey;

          // Hide the link
          getVoittaApiKeyLink.style.display = 'none';

          // Show success message
          alert('Successfully obtained Voitta API key!');
        })
        .catch((error) => {
          if (error.message !== 'Authentication cancelled') {
            console.error('Authentication error:', error);
            alert('Failed to authenticate. Please try again.');
          }
        });
    });
    voittaApiKeyGroup.appendChild(getVoittaApiKeyLink);

    // Add event listener to show/hide the link based on input value
    voittaApiKeyInput.addEventListener('input', () => {
      getVoittaApiKeyLink.style.display = voittaApiKeyInput.value ? 'none' : 'block';
    });

    form.appendChild(voittaApiKeyGroup);

    // OpenAI API Key field
    const openaiApiKeyGroup = this.createFormGroup(
      'escobar-openai-api-key',
      'OpenAI API Key',
      'Your OpenAI API key for OpenAI-powered features. (Optional)'
    );

    const openaiApiKeyInput = document.createElement('input');
    openaiApiKeyInput.id = 'escobar-openai-api-key';
    openaiApiKeyInput.className = 'escobar-settings-input';
    openaiApiKeyInput.type = 'text';
    openaiApiKeyInput.value = this.currentSettings.openaiApiKey || '';
    openaiApiKeyGroup.appendChild(openaiApiKeyInput);

    form.appendChild(openaiApiKeyGroup);

    // Anthropic API Key field
    const anthropicApiKeyGroup = this.createFormGroup(
      'escobar-anthropic-api-key',
      'Anthropic API Key',
      'Your Anthropic API key for Claude-powered features. (Optional)'
    );

    const anthropicApiKeyInput = document.createElement('input');
    anthropicApiKeyInput.id = 'escobar-anthropic-api-key';
    anthropicApiKeyInput.className = 'escobar-settings-input';
    anthropicApiKeyInput.type = 'text';
    anthropicApiKeyInput.value = this.currentSettings.anthropicApiKey || '';
    anthropicApiKeyGroup.appendChild(anthropicApiKeyInput);

    form.appendChild(anthropicApiKeyGroup);

    // Username field - editable in plugin environment
    const usernameGroup = this.createFormGroup(
      'escobar-username',
      'Username',
      'Your display name for chat messages.'
    );

    const usernameInput = document.createElement('input');
    usernameInput.id = 'escobar-username';
    usernameInput.className = 'escobar-settings-input';
    usernameInput.type = 'text';
    usernameInput.value = this.currentSettings.username;
    usernameGroup.appendChild(usernameInput);

    form.appendChild(usernameGroup);

    // Proxy Port field
    const proxyPortGroup = this.createFormGroup(
      'escobar-proxy-port',
      'Proxy Port',
      'The port number for the proxy server.'
    );

    const proxyPortInput = document.createElement('input');
    proxyPortInput.id = 'escobar-proxy-port';
    proxyPortInput.className = 'escobar-settings-input';
    proxyPortInput.type = 'number';
    proxyPortInput.min = '1';
    proxyPortInput.max = '65535';
    proxyPortInput.value = (this.currentSettings.proxyPort || 3000).toString();
    proxyPortGroup.appendChild(proxyPortInput);

    form.appendChild(proxyPortGroup);

    // Create buttons
    const buttonsContainer = this.createButtonsContainer();
    form.appendChild(buttonsContainer);

    container.appendChild(form);

    return container;
  }

  /**
   * Update form fields with current settings
   */
  protected updateFormFields(): void {
    // Get form elements
    const maxMessagesInput = document.getElementById('escobar-max-messages') as HTMLInputElement;
    const serverUrlInput = document.getElementById('escobar-server-url') as HTMLInputElement;
    const voittaApiKeyInput = document.getElementById('escobar-voitta-api-key') as HTMLInputElement;
    const openaiApiKeyInput = document.getElementById('escobar-openai-api-key') as HTMLInputElement;
    const anthropicApiKeyInput = document.getElementById('escobar-anthropic-api-key') as HTMLInputElement;
    const usernameInput = document.getElementById('escobar-username') as HTMLInputElement;
    const proxyPortInput = document.getElementById('escobar-proxy-port') as HTMLInputElement;

    // Update values with current settings
    if (maxMessagesInput) maxMessagesInput.value = this.currentSettings.maxMessages.toString();
    if (serverUrlInput) serverUrlInput.value = this.currentSettings.serverUrl;
    if (voittaApiKeyInput) voittaApiKeyInput.value = this.currentSettings.voittaApiKey || '';
    if (openaiApiKeyInput) openaiApiKeyInput.value = this.currentSettings.openaiApiKey || '';
    if (anthropicApiKeyInput) anthropicApiKeyInput.value = this.currentSettings.anthropicApiKey || '';
    if (usernameInput) usernameInput.value = this.currentSettings.username;
    if (proxyPortInput) proxyPortInput.value = (this.currentSettings.proxyPort || 3000).toString();
  }

  /**
   * Save settings changes
   */
  protected saveSettings(): void {
    // Get values from form
    const maxMessagesInput = document.getElementById('escobar-max-messages') as HTMLInputElement;
    const serverUrlInput = document.getElementById('escobar-server-url') as HTMLInputElement;
    const voittaApiKeyInput = document.getElementById('escobar-voitta-api-key') as HTMLInputElement;
    const openaiApiKeyInput = document.getElementById('escobar-openai-api-key') as HTMLInputElement;
    const anthropicApiKeyInput = document.getElementById('escobar-anthropic-api-key') as HTMLInputElement;
    const usernameInput = document.getElementById('escobar-username') as HTMLInputElement;
    const proxyPortInput = document.getElementById('escobar-proxy-port') as HTMLInputElement;

    // Validate and save settings
    this.validateAndSaveCommonSettings({
      maxMessages: parseInt(maxMessagesInput.value, 10),
      serverUrl: serverUrlInput.value.trim(),
      voittaApiKey: voittaApiKeyInput.value.trim(),
      openaiApiKey: openaiApiKeyInput.value.trim(),
      anthropicApiKey: anthropicApiKeyInput.value.trim(),
      username: usernameInput.value.trim(),
      proxyPort: proxyPortInput ? parseInt(proxyPortInput.value, 10) : 3000
    });
  }
}
