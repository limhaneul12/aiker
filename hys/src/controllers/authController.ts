import User from '../models/User'
import Joi from 'joi'

export const register = async (req, res) => {
    const schema = Joi.object({
        id: Joi.string().required(),
        password: Joi.string().required(),
        username: Joi.string().required(),
    })

    const validation = Joi.validate(req.body, schema)
    if (validation.error) {
        return res.send(validation.error.message)
    }

    try {
        const { id, password, username } = req.body
        const exists = await User.findOne({ id })
        if (exists) {
            return res.send('Already exists user id')
        }

        const user = await User.create({
            id,
            password,
            username,
        }).save()
        req.session.user = user
        return res.redirect('/')
    } catch (e) {
        console.error(e)
        return res.send('Error occurred')
    }
}

export const login = async (req, res) => {
    const schema = Joi.object({
        id: Joi.string().required(),
        password: Joi.string().required(),
    })

    const validation = Joi.validate(req.body, schema)
    if (validation.error) {
        return res.send(validation.error.message)
    }

    const { id, password } = req.body

    try {
        const user = await User.findOne({ id })
        if (!user) {
            return res.send('Not found id')
        }
        const isValidPassword = user.comparePassword(password)
        if (!isValidPassword) {
            return res.send('Invalid password')
        }
        req.session.user = user
        return res.redirect('/')
    } catch (e) {
        console.error(e)
        return res.send('Error occurred')
    }
}

export const logout = async (req, res) => {
    if (req.session.user) {
        req.session.destroy((err) => {
            if (err) {
                return res.send('Error occurred')
            }
        })
    }
    return res.redirect('/')
}
