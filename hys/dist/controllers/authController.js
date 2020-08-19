"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.logout = exports.login = exports.register = void 0;
const User_1 = __importDefault(require("../models/User"));
const joi_1 = __importDefault(require("joi"));
exports.register = (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const schema = joi_1.default.object({
        id: joi_1.default.string().required(),
        password: joi_1.default.string().required(),
        username: joi_1.default.string().required(),
    });
    const validation = joi_1.default.validate(req.body, schema);
    if (validation.error) {
        return res.send(validation.error.message);
    }
    try {
        const { id, password, username } = req.body;
        const exists = yield User_1.default.findOne({ id });
        if (exists) {
            return res.send('Already exists user id');
        }
        const user = yield User_1.default.create({
            id,
            password,
            username,
        }).save();
        req.session.user = user;
        return res.redirect('/');
    }
    catch (e) {
        console.error(e);
        return res.send('Error occurred');
    }
});
exports.login = (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const schema = joi_1.default.object({
        id: joi_1.default.string().required(),
        password: joi_1.default.string().required(),
    });
    const validation = joi_1.default.validate(req.body, schema);
    if (validation.error) {
        return res.send(validation.error.message);
    }
    const { id, password } = req.body;
    try {
        const user = yield User_1.default.findOne({ id });
        if (!user) {
            return res.send('Not found id');
        }
        const isValidPassword = user.comparePassword(password);
        if (!isValidPassword) {
            return res.send('Invalid password');
        }
        req.session.user = user;
        return res.redirect('/');
    }
    catch (e) {
        console.error(e);
        return res.send('Error occurred');
    }
});
exports.logout = (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    if (req.session.user) {
        req.session.destroy((err) => {
            if (err) {
                return res.send('Error occurred');
            }
        });
    }
    return res.redirect('/');
});
//# sourceMappingURL=authController.js.map