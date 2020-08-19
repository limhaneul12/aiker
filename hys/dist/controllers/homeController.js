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
exports.containerEditor = exports.search = exports.join = exports.home = void 0;
const Docker_1 = __importDefault(require("../models/Docker"));
exports.home = (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    // @ts-ignore
    if (req.session.user) {
        return res.render('index');
    }
    return res.render('index_login');
});
exports.join = (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    return res.render('index_join');
});
exports.search = (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    let dockers = [];
    let labels = [];
    try {
        const allDockers = yield Docker_1.default.find({
            order: { created_at: 'DESC' },
        });
        labels = allDockers.map((docker) => docker.label_idx);
        labels = [...new Set(labels)];
        dockers = yield Docker_1.default.find({
            where: {
                fk_user_id: req.session.user.idx,
            },
            order: { created_at: 'DESC' },
        });
    }
    catch (e) {
        console.error(e);
    }
    return res.render('search', {
        user_id: req.session.user.idx,
        dockers,
        labels,
    });
});
exports.containerEditor = (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    return res.render('con_editor');
});
//# sourceMappingURL=homeController.js.map