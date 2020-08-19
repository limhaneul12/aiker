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
exports.listByLabel = exports.remove = exports.read = exports.write = void 0;
const joi_1 = __importDefault(require("joi"));
const Docker_1 = __importDefault(require("../models/Docker"));
exports.write = (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const schema = joi_1.default.object({
        id: joi_1.default.string().required(),
        name: joi_1.default.string().required(),
        image: joi_1.default.string().required(),
        port: joi_1.default.string().required(),
        command: joi_1.default.string().required(),
        label_idx: joi_1.default.string().required(),
    });
    const validation = joi_1.default.validate(req.body, schema);
    if (validation.error) {
        return res.send(validation.error.message);
    }
    console.log(req.body);
    const { id, name, image, port, command, label_idx } = req.body;
    try {
        const exists = yield Docker_1.default.findOne({ id });
        if (exists) {
            return res.send('Already exists container id');
        }
        const docker = yield Docker_1.default.create({
            id,
            name,
            image,
            port,
            command,
            label_idx,
            fk_user_id: req.session.user.idx,
        }).save();
        console.log(docker);
        return res.redirect('/search');
    }
    catch (e) {
        console.error(e);
        return res.send('Error occurred');
    }
});
exports.read = (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const id = req.params.id;
    try {
        const docker = yield Docker_1.default.findOne({ id });
        if (!docker) {
            return res.send('Invalid container id');
        }
        return res.render('con', { docker });
    }
    catch (e) {
        console.error(e);
        return res.send('Error occurred');
    }
});
exports.remove = (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const id = req.params.id;
    try {
        const docker = yield Docker_1.default.findOne({ id });
        if (!docker) {
            return res.send('Not found docker');
        }
        if (docker.fk_user_id !== req.session.user.idx) {
            return res.send('No permission to remove this container');
        }
        yield docker.remove();
        return res.redirect('/search');
    }
    catch (e) {
        console.error(e);
        return res.send('Error occurred');
    }
});
exports.listByLabel = (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const label = req.params.label;
    console.log(label);
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
                label_idx: label,
            },
            order: { created_at: 'DESC' },
        });
    }
    catch (e) {
        console.error(e);
    }
    return res.render('search', {
        user_id: req.session.user.idx,
        labels,
        dockers,
    });
});
//# sourceMappingURL=dockerController.js.map