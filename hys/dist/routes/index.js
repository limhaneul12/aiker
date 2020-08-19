"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const docker_1 = __importDefault(require("./docker"));
const auth_1 = __importDefault(require("./auth"));
const home_1 = __importDefault(require("./home"));
const router = express_1.default.Router();
router.use('/', home_1.default);
router.use('/dockers', docker_1.default);
router.use('/auth', auth_1.default);
exports.default = router;
//# sourceMappingURL=index.js.map