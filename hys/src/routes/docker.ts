import express from 'express'
import * as dockerController from '../controllers/dockerController'
import checkAuth from '../lib/checkAuth'

const router = express.Router()

router.post('/', checkAuth, dockerController.write)
router.post('/delete/:id', checkAuth, dockerController.remove)

export default router
