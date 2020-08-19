import express from 'express'
import * as homeController from '../controllers/homeController'
import * as dockerController from '../controllers/dockerController'
import checkAuth from '../lib/checkAuth'

const router = express.Router()

router.get('/', homeController.home)
router.get('/join', homeController.join)
router.get('/search', checkAuth, homeController.search)
router.get('/con-editor', checkAuth, homeController.containerEditor)
router.get('/con/:id', checkAuth, dockerController.read)
router.get('/labels/:label', checkAuth, dockerController.listByLabel)

export default router
