"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const morgan_1 = __importDefault(require("morgan"));
const express_session_1 = __importDefault(require("express-session"));
const ejs_1 = __importDefault(require("ejs"));
const body_parser_1 = __importDefault(require("body-parser"));
const routes_1 = __importDefault(require("./routes"));
class App {
    constructor() {
        this.middlewares = () => {
            this.app.use(morgan_1.default('dev'));
            this.app.use(express_session_1.default({
                secret: process.env.SESSION_SECRET,
                resave: false,
                saveUninitialized: true,
            }));
            this.app.use(express_1.default.static(__dirname +
                (process.env.NODE_ENV === 'production'
                    ? '/../src/public'
                    : '/public')));
            this.app.set('view engine', 'ejs');
            this.app.set('views', __dirname +
                (process.env.NODE_ENV === 'production'
                    ? '/../src/views'
                    : '/views'));
            this.app.engine('html', ejs_1.default.renderFile);
            this.app.use(body_parser_1.default.json());
            this.app.use(body_parser_1.default.urlencoded({ extended: true }));
            this.app.use('/', routes_1.default);
        };
        this.app = express_1.default();
        this.middlewares();
    }
}
exports.default = App;
//# sourceMappingURL=app.js.map