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
var ExceptionSerializer_exports = {};
__export(ExceptionSerializer_exports, {
  ExceptionSerializer: () => ExceptionSerializer
});
module.exports = __toCommonJS(ExceptionSerializer_exports);
var import_CommandType = require("../CommandType.cjs");
var import_Command = require("../Command.cjs");
var import_RuntimeName = require("../RuntimeName.cjs");
var import_ExceptionType = require("../ExceptionType.cjs");
class ExceptionSerializer {
  static serializeException(exception, command) {
    let exceptionCommand = new import_Command.Command(import_RuntimeName.RuntimeName.Nodejs, import_CommandType.CommandType.Exception, []);
    exceptionCommand = exceptionCommand.addArgToPayload(this.getExceptionCode(exception));
    exceptionCommand = exceptionCommand.addArgToPayload(command.toString());
    exceptionCommand = exceptionCommand.addArgToPayload(exception.name);
    exceptionCommand = exceptionCommand.addArgToPayload(exception.message);
    let stackClasses = [];
    let stackMethods = [];
    let stackLines = [];
    let stackFiles = [];
    this.serializeStackTrace(exception, stackClasses, stackMethods, stackLines, stackFiles);
    exceptionCommand = exceptionCommand.addArgToPayload(stackClasses.join("|"));
    exceptionCommand = exceptionCommand.addArgToPayload(stackMethods.join("|"));
    exceptionCommand = exceptionCommand.addArgToPayload(stackLines.join("|"));
    exceptionCommand = exceptionCommand.addArgToPayload(stackFiles.join("|"));
    return exceptionCommand;
  }
  static getExceptionCode(exception) {
    switch (exception.name) {
      case "Error":
        return import_ExceptionType.ExceptionType.EXCEPTION;
      case "TypeError":
        return import_ExceptionType.ExceptionType.ILLEGAL_ARGUMENT_EXCEPTION;
      case "RangeError":
        return import_ExceptionType.ExceptionType.INDEX_OUT_OF_BOUNDS_EXCEPTION;
      default:
        return import_ExceptionType.ExceptionType.EXCEPTION;
    }
  }
  static serializeStackTrace(exception, stackClasses, stackMethods, stackLines, stackFiles) {
    const stackTrace = exception.stack.split("\n").slice(1);
    for (let i = 0; i < stackTrace.length; i++) {
      const parts = stackTrace[i].trim().match(/at\s(.*)\s\((.*):(\d+):(\d+)\)/);
      if (parts) {
        stackClasses.push(parts[1]);
        stackMethods.push("unknown");
        stackLines.push(parts[3]);
        stackFiles.push(parts[2]);
      } else {
        const parts2 = stackTrace[i].trim().match(/at\s(.*):(\d+):(\d+)/);
        if (parts2) {
          stackClasses.push("unknown");
          stackMethods.push("unknown");
          stackLines.push(parts2[2]);
          stackFiles.push(parts2[1]);
        }
      }
    }
  }
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  ExceptionSerializer
});
