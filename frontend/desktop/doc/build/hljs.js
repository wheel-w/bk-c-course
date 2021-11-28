/**
 * @file highlight.js 设置高亮语言，默认的加载的语言太多了
 * @author wheel-w
 */

import hljs from 'highlight.js/lib/highlight'

import bash from 'highlight.js/lib/languages/bash'
import css from 'highlight.js/lib/languages/css'
import javascript from 'highlight.js/lib/languages/javascript'

hljs.registerLanguage('bash', bash)
hljs.registerLanguage('css', css)
hljs.registerLanguage('javascript', javascript)

export default hljs
