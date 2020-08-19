const checkAuth = async (req, res, next) => {
    // @ts-ignore
    if (!req.session.user) {
        return res.redirect('/')
    }
    return next()
}

export default checkAuth
