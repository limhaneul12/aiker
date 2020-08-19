import {
    Entity,
    BaseEntity,
    PrimaryGeneratedColumn,
    Column,
    CreateDateColumn,
    UpdateDateColumn,
    BeforeInsert,
    BeforeUpdate,
} from 'typeorm'
import * as bcrypt from '../lib/bcrypt'

@Entity()
class User extends BaseEntity {
    @PrimaryGeneratedColumn()
    idx: number

    @Column({ length: 10, unique: true })
    id: string

    @Column({ length: 100 })
    password: string

    @Column({ length: 10 })
    username: string

    @CreateDateColumn()
    created_at: Date

    @UpdateDateColumn()
    updated_at: Date

    @BeforeInsert()
    @BeforeUpdate()
    async savePassword(): Promise<void> {
        if (this.password) {
            const hashed = await this.hashPassword(this.password)
            this.password = hashed
        }
    }

    public comparePassword(password: string): boolean {
        return bcrypt.compare(password, this.password)
    }

    private hashPassword(password: string): string {
        return bcrypt.hash(password)
    }
}

export default User
