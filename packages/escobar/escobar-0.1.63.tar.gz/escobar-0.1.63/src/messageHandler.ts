import { callPython, get_ws, PYTHON_CALL_EVENTS, stopped_messages } from './voitta/pythonBridge_browser';
import { functions, get_opened_tabs } from "./integrations/jupyter_integrations"
import MarkdownIt from 'markdown-it';
import sanitizeHtml from 'sanitize-html';
import hljs from 'highlight.js';
import markdownItHighlightjs from 'markdown-it-highlightjs';
import markdownItKatex from 'markdown-it-katex';
import markdownItQuestion from './markdown-it-question';

// Initialize markdown-it instance with all options enabled
const md = new MarkdownIt({
  html: true,        // Enable HTML tags in source
  breaks: true,      // Convert '\n' in paragraphs into <br>
  linkify: true,     // Autoconvert URL-like text to links
  typographer: true, // Enable some language-neutral replacement + quotes beautification
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, { language: lang, ignoreIllegals: true }).value;
      } catch (__) { }
    }
    return ''; // Use external default escaping
  }
});

// Enable all markdown-it features
md.enable('emphasis');       // For italic and bold
md.enable('link');           // For links
md.enable('heading');        // For headers
md.enable('code');           // For inline code
md.enable('fence');          // For code blocks
md.enable('blockquote');     // For blockquotes
md.enable('list');           // For lists
md.enable('table');          // For tables
md.enable('image');          // For images
md.enable('strikethrough');  // For strikethrough

// Use the highlight.js plugin for code syntax highlighting
md.use(markdownItHighlightjs);

// Use the KaTeX plugin for math rendering
md.use(markdownItKatex);

// Use the question plugin for interactive questions
md.use(markdownItQuestion);


// Add a wrapper around tables for better responsive behavior
const defaultRender = md.renderer.rules.table_open || function (tokens, idx, options, env, self) {
  return self.renderToken(tokens, idx, options);
};

md.renderer.rules.table_open = function (tokens, idx, options, env, self) {
  return '<div class="table-wrapper">' + defaultRender(tokens, idx, options, env, self);
};

const defaultRenderClose = md.renderer.rules.table_close || function (tokens, idx, options, env, self) {
  return self.renderToken(tokens, idx, options);
};

md.renderer.rules.table_close = function (tokens, idx, options, env, self) {
  return defaultRenderClose(tokens, idx, options, env, self) + '</div>';
};

// Improve image rendering by adding loading="lazy" and error handling
const defaultImageRender = md.renderer.rules.image || function (tokens, idx, options, env, self) {
  return self.renderToken(tokens, idx, options);
};

md.renderer.rules.image = function (tokens, idx, options, env, self) {
  // Get the token
  const token = tokens[idx];

  // Find the src attribute
  const srcIndex = token.attrIndex('src');
  const src = srcIndex >= 0 ? token.attrs[srcIndex][1] : '';

  // Add loading="lazy" attribute for better performance
  const loadingIndex = token.attrIndex('loading');
  if (loadingIndex < 0) {
    token.attrPush(['loading', 'lazy']);
  }

  // Add onerror handler to show a placeholder when image fails to load
  const onErrorIndex = token.attrIndex('onerror');
  if (onErrorIndex < 0) {
    token.attrPush(['onerror', "this.onerror=null;this.style.border='1px solid #ddd';this.style.padding='10px';this.style.width='auto';this.style.height='auto';this.alt='Image failed to load: ' + this.alt;this.src='data:image/svg+xml,%3Csvg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\"%3E%3Cpath fill=\"%23ccc\" d=\"M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z\"/%3E%3C/svg%3E';"]);
  }

  // Render the token with the added attributes
  return defaultImageRender(tokens, idx, options, env, self);
};

// Markdown-it is initialized and ready to use

// Configure sanitize-html options
const sanitizeOptions = {
  allowedTags: [
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'p', 'a', 'ul', 'ol',
    'nl', 'li', 'b', 'i', 'strong', 'em', 'strike', 'code', 'hr', 'br', 'div',
    'table', 'thead', 'caption', 'tbody', 'tr', 'th', 'td', 'pre', 'span', 'img',
    'button', // For question options
    // KaTeX elements
    'math', 'annotation', 'semantics', 'mrow', 'mn', 'mo', 'mi', 'mtext',
    'mspace', 'ms', 'mglyph', 'malignmark', 'mfrac', 'msqrt', 'mroot',
    'mstyle', 'merror', 'mpadded', 'mphantom', 'mfenced', 'menclose',
    'msub', 'msup', 'msubsup', 'munder', 'mover', 'munderover', 'mmultiscripts',
    'mtable', 'mtr', 'mtd', 'mlabeledtr', 'svg', 'path'
  ],
  allowedAttributes: {
    a: ['href', 'name', 'target', 'rel'],
    img: ['src', 'alt', 'title', 'width', 'height', 'loading', 'srcset', 'sizes', 'onerror', 'onload', 'style'],
    button: ['class', 'data-option', 'type', 'style'],
    code: ['class'],
    pre: ['class'],
    span: ['class', 'style'],
    '*': ['class', 'id', 'style', 'data-*']
  },
  selfClosing: ['img', 'br', 'hr', 'area', 'base', 'basefont', 'input', 'link', 'meta'],
  allowedSchemes: ['http', 'https', 'mailto', 'tel', 'data']
};


/**
 * A class representing a chat message
 */
export class ResponseMessage {
  public readonly id: string;
  public readonly role: 'user' | 'assistant' | 'action';
  public isNew: boolean;
  private messageElement: HTMLDivElement;
  private contentElement: HTMLDivElement;
  private content: string;
  private rawContent: string;

  /**
   * Create a new ResponseMessage
   * @param id Unique identifier for the message
   * @param role The role of the message sender ('user' or 'assistant')
   * @param initialContent Optional initial content for the message
   */
  constructor(id: string, role: 'user' | 'assistant' | 'action', initialContent: string = '') {
    this.id = id;
    this.role = role;
    this.isNew = true;
    this.content = initialContent;
    this.rawContent = initialContent;

    // Create message element
    this.messageElement = document.createElement('div');
    this.messageElement.className = `escobar-message escobar-message-${role}`;
    this.messageElement.dataset.messageId = id;

    // Create content element
    this.contentElement = document.createElement('div');
    this.contentElement.className = 'escobar-message-content markdown-content';

    // Set initial content with proper rendering for assistant and action messages
    if ((role === 'assistant' || role === 'action') && initialContent) {
      // Directly use markdown-it's HTML output without sanitization
      this.contentElement.innerHTML = md.render(initialContent);
    } else {
      this.contentElement.textContent = initialContent;
    }

    this.messageElement.appendChild(this.contentElement);
  }

  /**
   * Set the content of the message
   * @param content The new content
   */
  public setContent(content: string): void {
    this.content = content;
    this.rawContent = content;

    // Render markdown for assistant and action messages, keep plain text for user messages
    if (this.role === 'assistant' || this.role === 'action') {
      // Directly use markdown-it's HTML output without sanitization
      this.contentElement.innerHTML = md.render(content);

      // Log the rendered HTML for debugging
    } else {
      // For user messages, keep using textContent for security
      this.contentElement.textContent = content;
    }

    // Get the parent chat container and scroll to bottom
    const chatContainer = this.messageElement.closest('.escobar-chat-container');
    if (chatContainer) {
      setTimeout(() => {
        chatContainer.scrollTop = chatContainer.scrollHeight;
      }, 0);
    }
  }

  /**
   * Get the raw content of the message (original markdown)
   */
  public getRawContent(): string {
    return this.rawContent;
  }

  /**
   * Get the content of the message
   */
  public getContent(): string {
    return this.content;
  }

  /**
   * Get the DOM element for the message
   */
  public getElement(): HTMLDivElement {
    return this.messageElement;
  }
}

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
 * A class to handle message operations and storage
 */
export class MessageHandler {
  private messages: ResponseMessage[] = [];
  private messageMap: Map<string, ResponseMessage> = new Map();
  private static messageCounter = 0;
  private voittaApiKey: string;
  private openaiApiKey: string;
  private anthropicApiKey: string;
  private username: string;
  private chatContainer: HTMLDivElement;
  private maxMessages: number;

  /**
   * Create a new MessageHandler
   * @param voittaApiKey Voitta API key for authentication
   * @param openaiApiKey OpenAI API key for authentication
   * @param anthropicApiKey Anthropic API key for authentication
   * @param username Username for the current user
   * @param chatContainer DOM element to display messages
   * @param maxMessages Maximum number of messages to keep
   */
  constructor(voittaApiKey: string, openaiApiKey: string, anthropicApiKey: string, username: string, chatContainer: HTMLDivElement, maxMessages: number = 100) {
    this.voittaApiKey = voittaApiKey;
    this.openaiApiKey = openaiApiKey;
    this.anthropicApiKey = anthropicApiKey;
    this.username = username;
    this.chatContainer = chatContainer;
    this.maxMessages = maxMessages;

  }



  /**
   * Update the settings for the message handler
   * @param voittaApiKey New Voitta API key
   * @param openaiApiKey New OpenAI API key
   * @param anthropicApiKey New Anthropic API key
   * @param username New username
   * @param maxMessages New maximum messages
   */
  public updateSettings(voittaApiKey: string, openaiApiKey: string, anthropicApiKey: string, username: string, maxMessages: number): void {
    this.voittaApiKey = voittaApiKey;
    this.openaiApiKey = openaiApiKey;
    this.anthropicApiKey = anthropicApiKey;
    this.username = username;
    this.maxMessages = maxMessages;
  }

  /**
   * Generate a unique message ID
   */
  public generateMessageId(prefix: string = ""): string {
    const timestamp = Date.now();
    const counter = MessageHandler.messageCounter++;
    const messageId = `${prefix}-msg-${timestamp}-${counter}`;
    return messageId;
  }

  /**
   * Find a message by ID
   * @param id The message ID to find
   */
  public findMessageById(id: string): ResponseMessage | undefined {
    return this.messageMap.get(id);
  }

  /**
   * Add a message to the chat
   * @param role The role of the message sender ('user', 'assistant', or 'action')
   * @param content The message content
   * @param id Optional message ID (generated if not provided)
   * @returns The created ResponseMessage
   */
  public addMessage(role: 'user' | 'assistant' | 'action', content: string, id?: string): ResponseMessage {
    // Generate ID if not provided
    const messageId = id || this.generateMessageId();

    // Create a new ResponseMessage
    const message = new ResponseMessage(messageId, role, content);

    // Add to messages array
    this.messages.push(message);

    // Add to message map
    this.messageMap.set(messageId, message);

    // Add to DOM
    this.chatContainer.appendChild(message.getElement());

    // Scroll to bottom
    this.chatContainer.scrollTop = this.chatContainer.scrollHeight;

    // Limit the number of messages if needed
    this.limitMessages();

    return message;
  }

  /**
   * Limit the number of messages based on settings
   */
  public limitMessages(): void {
    if (this.messages.length > this.maxMessages) {
      // Remove excess messages
      const excessCount = this.messages.length - this.maxMessages;
      const removedMessages = this.messages.splice(0, excessCount);

      // Remove from DOM and message map
      for (const message of removedMessages) {
        this.chatContainer.removeChild(message.getElement());
        this.messageMap.delete(message.id);
      }
    }
  }

  /**
   * Clear all messages from the chat area
   */
  public async clearMessages(): Promise<void> {
    // Create a copy of the messages array to safely iterate through
    const messagesToRemove = [...this.messages];

    // Clear the original arrays first
    this.messages = [];

    // Now safely remove each message from the DOM and the map
    for (const message of messagesToRemove) {
      try {
        if (this.chatContainer.contains(message.getElement())) {
          this.chatContainer.removeChild(message.getElement());
        }
        this.messageMap.delete(message.id);
      } catch (error) {
        console.error('Error removing message:', error);
      }
    }

    // Clear the message map as a final safety measure
    this.messageMap.clear();
  }

  /**
   * Load messages from the server
   */
  public async loadMessages(): Promise<void> {
    const call_id = this.generateMessageId();
    const payload = JSON.stringify({
      method: "loadMessages",
      message: { machineId: this.username, "sessionId": "jupyter lab" },
      api_key: this.voittaApiKey,
      openai_api_key: this.openaiApiKey,
      anthropic_api_key: this.anthropicApiKey,
      call_id: call_id
    });

    const response = await callPython(payload);
    for (var i = 0; i < response.value.length; i++) {
      const message = response.value[i];
      switch (message.role) {
        case "user":
          if (typeof message.content === 'string' || message.content instanceof String) {
            this.addMessage('user', message.content);
          } else {
            /*
            for (var j = 0; j < message.content.length; j++) {
              const tp = message.content[j]["type"];
              if (tp == "tool_result") {
                this.addMessage('action', `> ${message.content[j]["name"]}`);
              }
            }
            */
            var a = 0;
          }
          break;
        case "assistant":
          if (typeof message.content === 'string' || message.content instanceof String) {
            this.addMessage('assistant', String(message.content))
          } else {
            if (message.content != undefined) {
              for (var j = 0; j < message.content.length; j++) {
                if (message.content[j]["type"] == "tool_use") {
                  const name = message.content[j]["name"];
                  this.addMessage('action', name);
                }
                var a = 0;
              }
            }
            break;
          }
        default:
        // Skip unknown message type
      }
    }
  }

  /**
   * Create a new chat session
   */
  public async createNewChat(): Promise<void> {
    const call_id = this.generateMessageId();
    const payload = JSON.stringify({
      method: "createNewChat",
      message: { machineId: this.username, "sessionId": "jupyter lab" },
      api_key: this.voittaApiKey,
      openai_api_key: this.openaiApiKey,
      anthropic_api_key: this.anthropicApiKey,
      call_id: call_id
    });

    await callPython(payload);
  }

  /**
   * Send a message to the server
   * @param content Message content
   * @param mode Message mode (Talk, Plan, Act)
   * @returns The response message
   */
  public async sendMessage(content: string, mode: string): Promise<ResponseMessage> {
    // Generate unique IDs for this message
    const userMessageId = this.generateMessageId();
    const messageId = this.generateMessageId();

    const opened_tabs = await get_opened_tabs();
    const current_notebook = await functions["listCells"].func()

    this.addMessage('user', content, userMessageId);

    // Create a placeholder response message with the same ID
    const responseMessage = this.addMessage('assistant', 'Waiting for response...', messageId);

    const ws = get_ws();

    // Send message to WebSocket server if connected
    if (ws && ws.readyState === WebSocket.OPEN) {
      try {
        const payload = JSON.stringify({
          method: "userMessage",
          message: content,
          opened_tabs: opened_tabs,
          current_notebook: current_notebook,
          mode: mode,
          api_key: this.voittaApiKey,
          openai_api_key: this.openaiApiKey,
          anthropic_api_key: this.anthropicApiKey,
          username: this.username,
          call_id: messageId
        });

        const response = await callPython(payload);
        this.handlePythonResponse(response, responseMessage);

      } catch (error) {
        if (error.stop != undefined) {
          stopped_messages[messageId] = true;
          const payload = JSON.stringify({
            method: "userStop",
            message_type: "request",
            api_key: this.voittaApiKey,
            openai_api_key: this.openaiApiKey,
            anthropic_api_key: this.anthropicApiKey,
            username: this.username,
            call_id: messageId
          });
          const response = await callPython(payload, 0, false);
          responseMessage.setContent('Interrupted by the user');
        } else {
          responseMessage.setContent('Error sending message to server');
        }
      }
    } else {
      // Fallback to echo response if not connected
      setTimeout(() => {
        responseMessage.setContent(`Echo: ${content} (WebSocket not connected)`);
      }, 500);
    }

    return responseMessage;
  }

  /**
   * Handle response from Python server
   * @param response Response data
   * @param responseMsg Response message to update
   */
  public handlePythonResponse(response: any, responseMsg?: ResponseMessage): void {
    try {
      let responseText: string;

      var value = response.value;

      if (typeof value === 'string') {
        responseText = value;
      } else if (value && typeof value === 'object') {
        responseText = JSON.stringify(value);
      } else {
        responseText = 'Received empty response from server';
      }

      // Update the response message with the content
      if (responseMsg) {
        responseMsg.setContent(responseText);
      }
    } catch (error) {
      console.error('Error handling Python response:', error);
      if (responseMsg) {
        responseMsg.setContent('Error: Failed to process server response');
      }
    }
  }

  /**
   * Get all messages
   */
  public getMessages(): ResponseMessage[] {
    return [...this.messages];
  }
}
