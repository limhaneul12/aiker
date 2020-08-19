"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const homeController = __importStar(require("../controllers/homeController"));
const dockerController = __importStar(require("../controllers/dockerController"));
const checkAuth_1 = __importDefault(require("../lib/checkAuth"));
const router = express_1.default.Router();
router.get('/', homeController.home);
router.get('/join', homeController.join);
router.get('/search', checkAuth_1.default, homeController.search);
router.get('/con-editor', checkAuth_1.default, homeController.containerEditor);
router.get('/con/:id', checkAuth_1.default, dockerController.read);
router.get('/labels/:label', checkAuth_1.default, dockerController.listByLabel);
exports.default = router;
//# sourceMappingURL=home.js.map