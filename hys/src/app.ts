import express from 'express'
import logger from 'morgan'
import session from 'express-session'
import ejs from 'ejs'
import bodyParser from 'body-parser'
import routes from './routes'

class App {
    public app

    constructor() {
        this.app = express()
        this.middlewares()
    }

    private middlewares = () => {
        this.app.use(logger('dev'))
        this.app.use(
            session({
                secret: process.env.SESSION_SECRET,
                resave: false,
                saveUninitialized: true,
            })
        )
        this.app.use(
            express.static(
                __dirname +
                    (process.env.NODE_ENV === 'production'
                        ? '/../src/public'
                        : '/public')
            )
        )
        this.app.set('view engine', 'ejs')
        this.app.set(
            'views',
            __dirname +
                (process.env.NODE_ENV === 'production'
                    ? '/../src/views'
                    : '/views')
        )
        this.app.engine('html', ejs.renderFile)
        this.app.use(bodyParser.json())
        this.app.use(bodyParser.urlencoded({ extended: true }))
        this.app.use('/', routes)
    }
}

export default App
