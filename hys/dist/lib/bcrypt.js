"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.compare = exports.hash = void 0;
const crypto_1 = __importDefault(require("crypto"));
exports.hash = (password) => {
    return crypto_1.default
        .createHmac('sha256', process.env.HASH_KEY || '')
        .update(password)
        .digest('hex');
};
exports.compare = (password, encrypted) => {
    return encrypted === exports.hash(password);
};
//# sourceMappingURL=bcrypt.js.map