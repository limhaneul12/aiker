import express from 'express'
import docker from './docker'
import auth from './auth'
import home from './home'

const router = express.Router()

router.use('/', home)
router.use('/dockers', docker)
router.use('/auth', auth)

export default router
