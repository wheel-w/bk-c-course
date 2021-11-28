/**
 * @file doc config
 * @author wheel-w
 */

import path from 'path'

export default {
    build: {
        assetsRoot: path.resolve(__dirname, '../dist-doc'),
        assetsSubDirectory: 'static',
        assetsPublicPath: './',
        productionSourceMap: true,
        productionGzip: false,
        productionGzipExtensions: ['js', 'css'],
        bundleAnalyzerReport: process.env.npm_config_report
    },
    dev: {
        assetsSubDirectory: 'static',
        assetsPublicPath: '/',
        cssSourceMap: false,
        autoOpenBrowser: true,
        localDocUrl: 'http://localhost',
        localDocPort: '8081'
    }
}
