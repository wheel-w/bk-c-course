/**
 * @file doc server
 * @author wheel-w
 */

import path from 'path'
import express from 'express'
import open from 'open'
import webpack from 'webpack'
import webpackDevMiddleware from 'webpack-dev-middleware'
import webpackHotMiddleware from 'webpack-hot-middleware'
import bodyParser from 'body-parser'

import docConf from './webpack.doc.conf'
import config from './config'

import checkVer from '../../build/check-versions'

checkVer()

const port = process.env.PORT || config.dev.localDocPort

const autoOpenBrowser = !!config.dev.autoOpenBrowser

const app = express()
const compiler = webpack(docConf)

const devMiddleware = webpackDevMiddleware(compiler, {
    publicPath: docConf.output.publicPath,
    quiet: true
})

const hotMiddleware = webpackHotMiddleware(compiler, {
    log: false,
    heartbeat: 2000
})

app.use(devMiddleware)

app.use(hotMiddleware)

app.use(bodyParser.json())

app.use(bodyParser.urlencoded({
    extended: true
}))

const staticPath = path.posix.join(config.dev.assetsPublicPath, config.dev.assetsSubDirectory)
app.use(staticPath, express.static('./static'))

const url = config.dev.localDocUrl + ':' + port

let _resolve
const readyPromise = new Promise(resolve => {
    _resolve = resolve
})

console.log('> Starting doc server...')
devMiddleware.waitUntilValid(() => {
    console.log('> Listening at ' + url + '\n')
    if (autoOpenBrowser) {
        open(url)
    }
    _resolve()
})

const server = app.listen(port)

export default {
    ready: readyPromise,
    close: () => {
        server.close()
    }
}
