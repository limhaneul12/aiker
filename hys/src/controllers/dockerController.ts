import Joi from 'joi'
import Docker from '../models/Docker'

export const write = async (req, res) => {
    const schema = Joi.object({
        id: Joi.string().required(),
        name: Joi.string().required(),
        image: Joi.string().required(),
        port: Joi.string().required(),
        command: Joi.string().required(),
        label_idx: Joi.string().required(),
    })
    const validation = Joi.validate(req.body, schema)
    if (validation.error) {
        return res.send(validation.error.message)
    }
    console.log(req.body)

    const { id, name, image, port, command, label_idx } = req.body

    try {
        const exists = await Docker.findOne({ id })
        if (exists) {
            return res.send('Already exists container id')
        }
        const docker = await Docker.create({
            id,
            name,
            image,
            port,
            command,
            label_idx,
            fk_user_id: req.session.user.idx,
        }).save()
        console.log(docker)
        return res.redirect('/search')
    } catch (e) {
        console.error(e)
        return res.send('Error occurred')
    }
}

export const read = async (req, res) => {
    const id = req.params.id
    try {
        const docker = await Docker.findOne({ id })
        if (!docker) {
            return res.send('Invalid container id')
        }
        return res.render('con', { docker })
    } catch (e) {
        console.error(e)
        return res.send('Error occurred')
    }
}

export const remove = async (req, res) => {
    const id = req.params.id
    try {
        const docker = await Docker.findOne({ id })
        if (!docker) {
            return res.send('Not found docker')
        }
        if (docker.fk_user_id !== req.session.user.idx) {
            return res.send('No permission to remove this container')
        }
        await docker.remove()
        return res.redirect('/search')
    } catch (e) {
        console.error(e)
        return res.send('Error occurred')
    }
}

export const listByLabel = async (req, res) => {
    const label = req.params.label
    console.log(label)
    let dockers: Docker[] = []
    let labels: string[] = []
    try {
        const allDockers = await Docker.find({
            order: { created_at: 'DESC' },
        })
        labels = allDockers.map((docker) => docker.label_idx)
        labels = [...new Set(labels)]
        dockers = await Docker.find({
            where: {
                label_idx: label,
            },
            order: { created_at: 'DESC' },
        })
    } catch (e) {
        console.error(e)
    }
    return res.render('search', {
        user_id: req.session.user.idx,
        labels,
        dockers,
    })
}
