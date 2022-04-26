/**
 * @file router 配置
 * @author wheel-w
 */

import http from '@/api'
import preload from '@/common/preload'
import store from '@/store'
import Vue from 'vue'
import VueRouter from 'vue-router'
Vue.use(VueRouter)

const MainEntry = () => import(/* webpackChunkName: 'entry' */'@/views')
const NotFound = () => import(/* webpackChunkName: 'none' */'@/views/404')
const Welcome = () => import('@/views/welcome')
const Home = () => import('@/views/home')
const Person = () => import('@/views/person')
const Mycourse = () => import('@/views/my_class/my_class_item/class_manage/my_course.vue')
const Coursenumber = () => import('@/views/my_class/my_class_item/class_manage/course_number.vue')
const CorrectPaper = () => import('@/views/my_class/my_class_item/class_manage/correct_paper')
const AnswerQuestionIndex = () => import('@/views/my_class/my_class_item/answer_question/answer_question_index')
const AnswerQuestionDetail = () => import('@/views/my_class/my_class_item/answer_question/answer_question_detail')
const SetQuestionIndex = () => import('@/views/my_class/my_class_item/set_question/set_question_index')
const Displaypaper = () => import('@/views/make_paper/display_paper.vue')
const Selectquestion = () => import('@/views/make_paper/select_question.vue')
const UserManage = () => import('@/views/userManage/userManage.vue')
const SetQuestion = () => import('@/views/set_question/set_question.vue')

const routes = [
    {
        path: window.PROJECT_CONFIG.SITE_URL,
        name: 'appMain',
        component: MainEntry,
        alias: '',
        children: [
            {
                path: 'welcome',
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
                alias: '',
                component: Home
            },
            {
                path: 'my_course',
                name: 'my_course',
                component: Mycourse
            },
            {
                path: 'course_number',
                name: 'course_number',
                component: Coursenumber
            },
            {
                path: 'answer_question_index',
                name: 'answer_question_index',
                component: AnswerQuestionIndex
            },
            {
                path: 'answer_question_detail',
                name: 'answer_question_detail',
                component: AnswerQuestionDetail
            },
            {
                path: 'correct_paper',
                name: 'correct_paper',
                component: CorrectPaper
            },
            {
                path: 'set_question_index',
                name: 'set_question_index',
                component: SetQuestionIndex
            },
            {
                path: 'displaypaper',
                name: 'displaypaper',
                component: Displaypaper
            },
            {
                path: 'selectquestion',
                name: 'selectquestion',
                component: Selectquestion
            },
            {
                path: 'userManage',
                name: 'userManage',
                component: UserManage
            },
            {
                path: 'set_question',
                name: 'set_question',
                component: SetQuestion
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
