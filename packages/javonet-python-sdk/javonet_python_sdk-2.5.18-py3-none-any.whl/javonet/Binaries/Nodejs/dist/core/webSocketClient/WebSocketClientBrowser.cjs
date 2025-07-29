"use strict";
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);
var WebSocketClientBrowser_exports = {};
__export(WebSocketClientBrowser_exports, {
  WebSocketClientBrowser: () => WebSocketClientBrowser
});
module.exports = __toCommonJS(WebSocketClientBrowser_exports);
var import_Runtime = require("../../utils/Runtime.cjs");
const WebSocketState = (
  /** @type {const} */
  {
    OPEN: "open",
    CLOSE: "close",
    ERROR: "error",
    MESSAGE: "message"
  }
);
let WsClient = null;
if ((0, import_Runtime.isBrowserRuntime)()) {
  WsClient = WebSocket;
}
class WebSocketClientBrowser {
  /**
   * @param {string} url
   * @param {Options} [options]
   */
  constructor(url, options) {
    this.url = url;
    this.instance = null;
    this.isConnected = false;
    this.isDisconnectedAfterMessage = options?.isDisconnectedAfterMessage ?? false;
  }
  /**
   * Sends messageArray through websocket connection
   * @async
   * @param {Int8Array} messageArray
   * @returns {Promise<Int8Array>}
   */
  send(messageArray) {
    return new Promise((resolve, reject) => {
      try {
        if (this.isConnected) {
          this._sendMessage(messageArray, resolve, reject);
        } else {
          this._connect().then(() => {
            this._sendMessage(messageArray, resolve, reject);
          });
        }
      } catch (error) {
        reject(error);
      }
    });
  }
  /**
   * Disconnects the WebSocket by terminating the connection.
   * @returns {void}
   *
   */
  disconnect() {
    if (this.instance) {
      this.instance.close();
    }
    this.isConnected = false;
  }
  /**
   * Connects to the WebSocket server.
   * @private
   * @async
   * @returns {Promise<void>} - A promise that resolves when the connection is established.
   */
  _connect() {
    return new Promise((resolve, reject) => {
      if (WsClient === null) {
        return reject(new Error("missing WebSocket client"));
      }
      this.instance = new WsClient(this.url);
      this.instance.binaryType = "arraybuffer";
      this.instance.addEventListener(WebSocketState.OPEN, () => {
        this.isConnected = true;
        resolve();
      });
      this.instance.addEventListener(WebSocketState.ERROR, (error) => {
        reject(error);
      });
      this.instance.addEventListener(WebSocketState.CLOSE, () => {
        this.isConnected = false;
      });
    });
  }
  /**
   * Sends the data to the WebSocket server and listens for a response.
   * @private
   * @async
   * @param {Int8Array} data - The data to send.
   * @param {Function} resolve - The resolve function for the Promise.
   * @param {Function} reject - The reject function for the Promise.
   * @returns {void}
   */
  _sendMessage(data, resolve, reject) {
    try {
      if (this.instance === null || !this.instance) {
        throw new Error("error websocket not connected");
      }
      const arrayBuffer = data.buffer;
      this.instance.send(arrayBuffer);
      const handleMessage = (msg) => {
        if (this.instance === null || !this.instance) {
          throw new Error("error websocket not connected");
        }
        const byteArray = new Int8Array(msg.data);
        resolve(byteArray);
        if (this.isDisconnectedAfterMessage) {
          this.disconnect();
        }
        this.instance.removeEventListener(WebSocketState.MESSAGE, handleMessage);
        this.instance.removeEventListener(WebSocketState.ERROR, handleError);
      };
      const handleError = (error) => {
        reject(error);
        if (this.instance) {
          this.instance.removeEventListener(WebSocketState.MESSAGE, handleMessage);
          this.instance.removeEventListener(WebSocketState.ERROR, handleError);
        }
      };
      if (this.instance) {
        this.instance.addEventListener(WebSocketState.MESSAGE, handleMessage);
        this.instance.addEventListener(WebSocketState.ERROR, handleError);
      }
    } catch (err) {
      reject(err);
    }
  }
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  WebSocketClientBrowser
});
