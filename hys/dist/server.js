"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const app_1 = __importDefault(require("./app"));
require("./env");
const typeorm_1 = require("typeorm");
const db_1 = __importDefault(require("./db"));
const { PORT } = process.env;
const app = new app_1.default().app;
typeorm_1.createConnection(db_1.default)
    .then(() => {
    app.listen(PORT, () => {
        console.log(`Listening server on port ${PORT}`);
    });
})
    .catch((error) => console.error(error));
//# sourceMappingURL=server.js.map