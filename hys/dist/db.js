"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const connectionOptions = {
    type: 'mysql',
    host: process.env.DB_ENDPOINT,
    port: Number(process.env.DB_PORT),
    username: process.env.DB_USERNAME,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    entities: ['models/**/*.*'],
    synchronize: true,
    logging: true,
};
exports.default = connectionOptions;
//# sourceMappingURL=db.js.map