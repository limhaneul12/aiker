import App from './app'
import './env'
import { createConnection } from 'typeorm'
import connectionOptions from './db'

const { PORT } = process.env
const app = new App().app

createConnection(connectionOptions)
    .then(() => {
        app.listen(PORT, () => {
            console.log(`Listening server on port ${PORT}`)
        })
    })
    .catch((error) => console.error(error))
