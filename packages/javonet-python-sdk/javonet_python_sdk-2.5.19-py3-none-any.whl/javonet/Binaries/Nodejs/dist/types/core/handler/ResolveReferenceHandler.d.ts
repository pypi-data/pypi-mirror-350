export type Command = import("../../utils/Command.js").Command;
/**
 * @typedef {import('../../utils/Command.js').Command} Command
 */
export class ResolveReferenceHandler extends AbstractHandler {
    /**
     * @param {Command} command
     * @returns {any}
     */
    process(command: Command): any;
}
import { AbstractHandler } from './AbstractHandler.js';
