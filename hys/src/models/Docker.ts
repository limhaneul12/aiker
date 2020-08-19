import {
    Entity,
    BaseEntity,
    PrimaryGeneratedColumn,
    Column,
    CreateDateColumn,
    UpdateDateColumn,
    ManyToOne,
    JoinColumn,
} from 'typeorm'
import User from './User'

@Entity()
class Docker extends BaseEntity {
    @PrimaryGeneratedColumn()
    idx: number

    @Column({ length: 100, unique: true })
    id: string

    @Column({ length: 100 })
    name: string

    @Column({ length: 255 })
    image: string

    @Column({ length: 50 })
    port: string

    @Column({ length: 100 })
    command: string

    @Column({ length: 10 })
    label_idx: string

    @CreateDateColumn()
    created_at: Date

    @UpdateDateColumn()
    updated_at: Date

    @ManyToOne((type) => User, { onDelete: 'CASCADE' })
    @JoinColumn({ name: 'fk_user_id' })
    user: User

    @Column({ type: 'int' })
    fk_user_id: string
}

export default Docker
