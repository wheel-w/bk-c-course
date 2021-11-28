/**
 * @file webpack doc conf
 * @author wheel-w
 */

import path from 'path'

import webpack from 'webpack'
import merge from 'webpack-merge'
import HtmlWebpackPlugin from 'html-webpack-plugin'
import FriendlyErrorsPlugin from 'friendly-errors-webpack-plugin'

import manifest from '../../static/lib-manifest.json'
import baseConf from '../../build/webpack.base.conf'
import mdLoaderOption from './md-loader-option'

const webpackConfig = merge(baseConf, {
    mode: 'development',
    entry: {
        main: './doc/main.js'
    },

    module: {
        rules: [
            {
                test: /\.(css|postcss)$/,
                use: [
                    'vue-style-loader',
                    {
                        loader: 'css-loader',
                        options: {
                            importLoaders: 1
                        }
                    },
                    {
                        loader: 'postcss-loader',
                        options: {
                            config: {
                                path: path.resolve(__dirname, '../..', 'postcss.config.js')
                            }
                        }
                    }
                ]
            },
            {
                test: /\.md$/,
                use: [
                    {
                        loader: 'vue-loader'
                    },
                    {
                        loader: 'vue-markdown-loader/lib/markdown-compiler',
                        options: mdLoaderOption
                    }
                ]
            }
        ]
    },

    plugins: [
        new webpack.DllReferencePlugin({
            context: __dirname,
            manifest: manifest
        }),

        new webpack.HotModuleReplacementPlugin(),

        new webpack.NoEmitOnErrorsPlugin(),

        new HtmlWebpackPlugin({
            filename: 'index.html',
            template: path.resolve(__dirname, '../doc-tmpl.html'),
            inject: true
        }),

        new FriendlyErrorsPlugin()
    ]
})

Object.keys(webpackConfig.entry).forEach(name => {
    webpackConfig.entry[name] = ['./build/dev-client'].concat(webpackConfig.entry[name])
})

export default webpackConfig
