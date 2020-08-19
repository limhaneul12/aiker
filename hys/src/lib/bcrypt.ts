import crypto from 'crypto'

export const hash = (password: string): string => {
    return crypto
        .createHmac('sha256', process.env.HASH_KEY || '')
        .update(password)
        .digest('hex')
}

export const compare = (password: string, encrypted: string): boolean => {
    return encrypted === hash(password)
}
