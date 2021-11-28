/**
 * @file build doc
 * @author wheel-w
 */

import ora from 'ora'
import chalk from 'chalk'
import webpack from 'webpack'
import rm from 'rimraf'

import webpackConf from './webpack.doc.prod.conf'
import config from './config'

import checkVer from '../../build/check-versions'

checkVer()

const spinner = ora('building doc...')
spinner.start()

rm(config.build.assetsRoot, e => {
    if (e) {
        throw e
    }
    webpack(webpackConf, (err, stats) => {
        spinner.stop()
        if (err) {
            throw err
        }
        process.stdout.write(stats.toString({
            colors: true,
            modules: false,
            children: false,
            chunks: false,
            chunkModules: false
        }) + '\n\n')

        if (stats.hasErrors()) {
            console.log(chalk.red('  Build Doc failed with errors.\n'))
            process.exit(1)
        }

        console.log(chalk.cyan('  Build Doc complete.\n'))
        console.log(chalk.yellow(
            '  Tip: built files are meant to be served over an HTTP server.\n'
            + '  Opening index.html over file:// won\'t work.\n'
        ))
    })
})
