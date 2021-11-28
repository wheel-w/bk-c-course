/**
 * @file vue-markdown-loader conf
 * @author wheel-w
 */

import markdownItContainer from 'markdown-it-container'
import MarkdownIt from 'markdown-it'
import markdownItAnchor from 'markdown-it-anchor'
import markdownItAttrs from 'markdown-it-attrs'
import { slugify } from 'transliteration'

import markdownItHighlightjs from './md-highlight'

const md = new MarkdownIt({
    html: true,
    linkify: true,
    typographer: true
})

const position = {
    false: 'push',
    true: 'unshift'
}

const createTips = cls => {
    return [markdownItContainer, cls, {
        render: (tokens, idx) => {
            const token = tokens[idx]
            const title = token.info.trim().slice(cls.length).trim() || ''
            if (token.nesting === 1) {
                if (title) {
                    return `<div class="${cls} tips-block with-title"><p class="tips-block-title">${title}</p>\n`
                }
                return `<div class="${cls} tips-block">\n`
            }
            return '</div>\n'
        }
    }]
}

export default {
    raw: true,
    preventExtract: true,
    use: [
        [markdownItHighlightjs],
        [markdownItAttrs],
        [markdownItAnchor, {
            level: 3,
            slugify: slugify,
            permalink: true,
            permalinkBefore: true,
            permalinkClass: 'header-anchor',
            permalinkSymbol: '<svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg>',
            permalinkHref: (slug, state) => {
                return `?anchor=${slug}`
            },
            renderPermalink: (slug, opts, state, idx) => {
                const space = () => Object.assign(new state.Token('text', '', 0), { content: ' ' })
                const attrs = state.tokens[idx].attrs

                const href = attrs[0][0] === 'page'
                    ? attrs[0][1] + opts.permalinkHref(slug, state)
                    : opts.permalinkHref(slug, state)

                const linkTokens = [
                    Object.assign(new state.Token('link_open', 'a', 1), {
                        attrs: [
                            ['class', opts.permalinkClass],
                            ['href', href],
                            ['aria-hidden', 'true'],
                            ['anchor-link', slug]
                        ]
                    }),
                    Object.assign(new state.Token('html_block', '', 0), { content: opts.permalinkSymbol }),
                    new state.Token('link_close', 'a', -1)
                ]

                linkTokens[position[!opts.permalinkBefore]](space())
                state.tokens[idx + 1].children[position[opts.permalinkBefore]](...linkTokens)
            }
        }],
        createTips('tip'),
        createTips('info'),
        createTips('warning'),
        createTips('danger'),
        [markdownItContainer, 'exampleLink', {
            validate: params => {
                return params.trim().match(/^exampleLink\s*(.*)$/)
            },
            render: (tokens, idx) => {
                const m = tokens[idx].info.trim().match(/^exampleLink\s*(.*)$/)

                if (tokens[idx].nesting === 1) {
                    const description = (m && m.length > 1) ? m[1] : ''
                    const descriptionHTML = description ? md.render(description) : ''
                    return `<div class="example-link">${descriptionHTML}</div>`
                }
                return ''
            }
        }],
        [markdownItContainer, 'changelogVer', {
            validate: params => {
                return params.trim().match(/^changelogVer\s*(.*)$/)
            },
            render: (tokens, idx) => {
                const m = tokens[idx].info.trim().match(/^changelogVer\s*(.*)$/)

                if (tokens[idx].nesting === 1) {
                    const description = (m && m.length > 1) ? m[1] : ''
                    const descriptionHTML = description ? md.renderInline(description) : ''
                    const idAttr = /v=([^)]*)/.test(description)
                        ? ` id="${RegExp.$1}"`
                        : ''
                    return `<h3${idAttr}>${descriptionHTML}</h3>`
                }
                return ''
            }
        }]
    ]
}
