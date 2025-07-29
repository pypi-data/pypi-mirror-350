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
var WebSocketClient_exports = {};
__export(WebSocketClient_exports, {
  WebSocketClient: () => WebSocketClient
});
module.exports = __toCommonJS(WebSocketClient_exports);
var import_Runtime = require("../../utils/Runtime.cjs");
const import_meta = {};
const requireDynamic = (0, import_Runtime.getRequire)(import_meta.url);
const WebSocketStateEnum = {
  OPEN: "open",
  CLOSE: "close",
  ERROR: "error"
};
let WebSocket = null;
class WebSocketClient {
  /**
   * @param {string} url
   * @param {{ isDisconnectedAfterMessage: boolean }} options
   */
  constructor(url, options) {
    this.url = url;
    this.instance = null;
    this.isConnected = false;
    this.isDisconnectedAfterMessage = options?.isDisconnectedAfterMessage ?? true;
  }
  /**
   * Connects to the WebSocket server.
   * @async
   * @returns {Promise<wsClient>} - A promise that resolves when the connection is established.
   */
  async connect() {
    if (!WebSocket) {
      if ((0, import_Runtime.isNodejsRuntime)()) {
        try {
          WebSocket = requireDynamic("ws");
        } catch (error) {
          if (typeof error === "object" && error && "code" in error && error.code === "MODULE_NOT_FOUND") {
            throw new Error("ws module not found. Please install it using npm install ws");
          }
          throw error;
        }
      }
    }
    return new Promise((resolve, reject) => {
      if (!WebSocket) {
        reject(new Error("ws client is null"));
        return;
      }
      const client = new WebSocket(this.url);
      client.on(WebSocketStateEnum.OPEN, () => {
        this.instance = client;
        resolve(client);
      });
      client.on(WebSocketStateEnum.ERROR, (error) => {
        reject(error);
      });
      client.on(WebSocketStateEnum.CLOSE, () => {
        reject(new Error("Connection closed before receiving message"));
      });
    });
  }
  /**
   * Sends messageArray through websocket connection
   * @async
   * @param {Int8Array} messageArray
   * @returns {Promise<Int8Array>}
   */
  send(messageArray) {
    return new Promise((resolve, reject) => {
      ;
      (this.instance ? Promise.resolve(this.instance) : this._connect()).then((client) => {
        client.send(
          /** @type {any} */
          messageArray
        );
        client.on("message", (message) => {
          resolve(message);
          if (this.isDisconnectedAfterMessage) {
            this.disconnect();
          }
        });
      }).catch((error) => {
        reject(error);
      });
    });
  }
  /**
   * Disconnects the WebSocket by terminating the connection.
   */
  disconnect() {
    if (this.instance) {
      this.instance.close();
      this.instance = null;
    }
    this.isConnected = false;
  }
  /**
   * Connects to the WebSocket server.
   * @private
   * @async
   * @returns {Promise<wsClient>} - A promise that resolves when the connection is established.
   */
  _connect() {
    if (!WebSocket) {
      if ((0, import_Runtime.isNodejsRuntime)()) {
        try {
          WebSocket = requireDynamic("ws");
        } catch (error) {
          if (
            /** @type {{ code?: string }} */
            error.code === "MODULE_NOT_FOUND"
          ) {
            throw new Error("ws module not found. Please install it using npm install ws");
          }
          throw error;
        }
      }
    }
    return new Promise((resolve, reject) => {
      if (!WebSocket) {
        reject(new Error("ws client is null"));
        return;
      }
      const client = new WebSocket(this.url);
      client.on(WebSocketStateEnum.OPEN, () => {
        this.isConnected = true;
        this.instance = client;
        resolve(client);
      });
      client.on(WebSocketStateEnum.ERROR, (error) => {
        reject(error);
      });
      client.on(WebSocketStateEnum.CLOSE, () => {
        reject(new Error("Connection closed before receiving message"));
      });
    });
  }
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  WebSocketClient
});
