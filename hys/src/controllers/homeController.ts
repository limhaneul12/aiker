import Docker from '../models/Docker'

export const home = async (req, res) => {
    // @ts-ignore
    if (req.session.user) {
        return res.render('index')
    }

    return res.render('index_login')
}

export const join = async (req, res) => {
    return res.render('index_join')
}

export const search = async (req, res) => {
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
                fk_user_id: req.session.user.idx,
            },
            order: { created_at: 'DESC' },
        })
    } catch (e) {
        console.error(e)
    }
    return res.render('search', {
        user_id: req.session.user.idx,
        dockers,
        labels,
    })
}

export const containerEditor = async (req, res) => {
    return res.render('con_editor')
}
