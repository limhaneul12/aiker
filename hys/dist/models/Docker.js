"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const typeorm_1 = require("typeorm");
const User_1 = __importDefault(require("./User"));
let Docker = class Docker extends typeorm_1.BaseEntity {
};
__decorate([
    typeorm_1.PrimaryGeneratedColumn(),
    __metadata("design:type", Number)
], Docker.prototype, "idx", void 0);
__decorate([
    typeorm_1.Column({ length: 100, unique: true }),
    __metadata("design:type", String)
], Docker.prototype, "id", void 0);
__decorate([
    typeorm_1.Column({ length: 100 }),
    __metadata("design:type", String)
], Docker.prototype, "name", void 0);
__decorate([
    typeorm_1.Column({ length: 255 }),
    __metadata("design:type", String)
], Docker.prototype, "image", void 0);
__decorate([
    typeorm_1.Column({ length: 50 }),
    __metadata("design:type", String)
], Docker.prototype, "port", void 0);
__decorate([
    typeorm_1.Column({ length: 100 }),
    __metadata("design:type", String)
], Docker.prototype, "command", void 0);
__decorate([
    typeorm_1.Column({ length: 10 }),
    __metadata("design:type", String)
], Docker.prototype, "label_idx", void 0);
__decorate([
    typeorm_1.CreateDateColumn(),
    __metadata("design:type", Date)
], Docker.prototype, "created_at", void 0);
__decorate([
    typeorm_1.UpdateDateColumn(),
    __metadata("design:type", Date)
], Docker.prototype, "updated_at", void 0);
__decorate([
    typeorm_1.ManyToOne((type) => User_1.default, { onDelete: 'CASCADE' }),
    typeorm_1.JoinColumn({ name: 'fk_user_id' }),
    __metadata("design:type", User_1.default)
], Docker.prototype, "user", void 0);
__decorate([
    typeorm_1.Column({ type: 'int' }),
    __metadata("design:type", String)
], Docker.prototype, "fk_user_id", void 0);
Docker = __decorate([
    typeorm_1.Entity()
], Docker);
exports.default = Docker;
//# sourceMappingURL=Docker.js.map