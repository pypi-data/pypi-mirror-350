export type Options = {
    isDisconnectedAfterMessage: boolean;
};
/**
 * @typedef {object} Options
 * @property {boolean} isDisconnectedAfterMessage
 */
/**
 * WebSocketClient class that handles WebSocket connection, message sending, and automatic disconnection.
 */
export class WebSocketClientBrowser {
    /**
     * @param {string} url
     * @param {Options} [options]
     */
    constructor(url: string, options?: Options);
    /**
     * @type {string}
     */
    url: string;
    /**
     * @type {WebSocket | null}
     */
    instance: WebSocket | null;
    /**
     * @type {boolean} isConnected indicates whether the WebSocket is connected.
     */
    isConnected: boolean;
    /**
     * @type {boolean}
     */
    isDisconnectedAfterMessage: boolean;
    /**
     * Sends messageArray through websocket connection
     * @async
     * @param {Int8Array} messageArray
     * @returns {Promise<Int8Array>}
     */
    send(messageArray: Int8Array): Promise<Int8Array>;
    /**
     * Disconnects the WebSocket by terminating the connection.
     * @returns {void}
     *
     */
    disconnect(): void;
    /**
     * Connects to the WebSocket server.
     * @private
     * @async
     * @returns {Promise<void>} - A promise that resolves when the connection is established.
     */
    private _connect;
    /**
     * Sends the data to the WebSocket server and listens for a response.
     * @private
     * @async
     * @param {Int8Array} data - The data to send.
     * @param {Function} resolve - The resolve function for the Promise.
     * @param {Function} reject - The reject function for the Promise.
     * @returns {void}
     */
    private _sendMessage;
}
