/**
 * @file router 配置
 * @author wheel-w
 */

import Vue from 'vue'
import VueRouter from 'vue-router'

import store from '@/store'
import http from '@/api'
import preload from '@/common/preload'

Vue.use(VueRouter)

const MainEntry = () => import(/* webpackChunkName: 'entry' */'@/views')
const NotFound = () => import(/* webpackChunkName: 'none' */'@/views/404')
const Welcome = () => import('@/views/welcome')
const Home = () => import('@/views/home')
const Person = () => import('@/views/person')
const Classmanage = () => import('@/views/class_manage')
const SetQuestion = () => import('@/views/class_manage/class_manage_item/set_question')
const MyManageClass = () => import('@/views/class_manage/class_manage_item/my_manage_class')
const Myclass = () => import('@/views/my_class')
const MyJoinClass = () => import('@/views/my_class/my_class_item/my_join_class')
const MyJoinClassDetail = () => import('@/views/my_class/my_class_item/my_join_class_detail')
const AnswerQuestion = () => import('@/views/my_class/my_class_item/answer_question')

const routes = [
    {
        path: window.PROJECT_CONFIG.SITE_URL,
        name: 'appMain',
        component: MainEntry,
        alias: '',
        children: [
            {
                path: 'welcome',
                alias: '',
                name: 'welcome',
                component: Welcome
            },
            {
                path: 'person',
                name: 'person',
                component: Person
            },
            {
                path: 'home',
                name: 'home',
                component: Home
            },
            {
                path: 'class_manage',
                name: 'class_manage',
                component: Classmanage,
                children: [
                    {
                        path: 'set_question',
                        name: 'set_question',
                        component: SetQuestion
                    },
                    {
                        path: 'my_manage_class',
                        name: 'my_manage_class',
                        component: MyManageClass
                    }
                ]
            },
            {
                path: 'my_class',
                name: 'my_class',
                component: Myclass,
                children: [
                    {
                        path: 'my_join_class',
                        name: 'my_join_class',
                        component: MyJoinClass
                    },
                    {
                        path: 'my_join_class_detail',
                        name: 'my_join_class_detail',
                        component: MyJoinClassDetail
                    },
                    {
                        path: 'answer_question',
                        name: 'answer_question',
                        component: AnswerQuestion
                    }
                ]
            }
        ]
    },
    // 404
    {
        path: '*',
        name: '404',
        component: NotFound
    }
]

const router = new VueRouter({
    mode: 'history',
    routes: routes
})

const cancelRequest = async () => {
    const allRequest = http.queue.get()
    const requestQueue = allRequest.filter(request => request.cancelWhenRouteChange)
    await http.cancel(requestQueue.map(request => request.requestId))
}

let preloading = true
let canceling = true
let pageMethodExecuting = true

router.beforeEach(async (to, from, next) => {
    canceling = true
    await cancelRequest()
    canceling = false
    next()
})

router.afterEach(async (to, from) => {
    store.commit('setMainContentLoading', true)

    preloading = true
    await preload()
    preloading = false

    const pageDataMethods = []
    const routerList = to.matched
    routerList.forEach(r => {
        Object.values(r.instances).forEach(vm => {
            if (typeof vm.fetchPageData === 'function') {
                pageDataMethods.push(vm.fetchPageData())
            }
            if (typeof vm.$options.preload === 'function') {
                pageDataMethods.push(vm.$options.preload.call(vm))
            }
        })
    })

    pageMethodExecuting = true
    await Promise.all(pageDataMethods)
    pageMethodExecuting = false

    if (!preloading && !canceling && !pageMethodExecuting) {
        store.commit('setMainContentLoading', false)
    }
})

export default router
