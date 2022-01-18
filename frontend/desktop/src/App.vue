<template>
    <div class="monitor-navigation" :class="systemCls">
        <bk-navigation
            :header-title="nav.id"
            :side-title="nav.title"
            :default-open="true"
            :navigation-type="'top-bottom'"
            :need-menu="true"
            @toggle="handleToggle">
            <template slot="header">
                <div class="monitor-navigation-header">
                    <ol class="header-nav">
                        <bk-popover v-for="(item,index) in header.list" :key="item.id" theme="light navigation-message" :arrow="false" offset="0, -5" placement="bottom" :tippy-options="{ 'hideOnClick': false, flipBehavior: ['bottom'] }">
                            <li v-show="item.show" class="header-nav-item" :class="{ 'item-active': index === header.active }">
                                {{item.name}}
                            </li>
                            <template slot="content">
                                <ul class="monitor-navigation-nav">
                                    <li class="nav-item" v-for="headerNavItem in curHeaderNav.navList" :key="headerNavItem.id">
                                        {{headerNavItem.name}}
                                    </li>
                                </ul>
                            </template>
                        </bk-popover>
                    </ol>
                    <div class="header-select">
                    </div>
                    <bk-popover theme="light navigation-message" :arrow="false" offset="-20, 10" placement="bottom-start" :tippy-options="{ 'hideOnClick': false }">
                        <div class="header-user">
                            admin
                            <i class="bk-icon icon-down-shape"></i>
                        </div>
                        <template slot="content">
                            <ul class="monitor-navigation-admin">
                                <li class="nav-item" v-for="userItem in user.list" :key="userItem" @click="handleSelect(userItem.id,userItem)">
                                    {{userItem.name}}
                                </li>
                            </ul>
                        </template>
                    </bk-popover>
                </div>
            </template>
            <template slot="menu">
                <bk-navigation-menu
                    ref="menu"
                    @select="handleSelect"
                    :default-active="nav.id"
                    :toggle-active="nav.toggle">
                    <bk-navigation-menu-item
                        v-for="item in nav.list"
                        :has-child="item.children.length === 0 ? false : true"
                        :key="item.id"
                        :default-active="item.active"
                        v-bind="item">
                        <span>{{item.name}}</span>
                        <div slot="child">
                            <bk-navigation-menu-item
                                v-for="child in item.children"
                                :key="child.id"
                                v-bind="child">
                                <span>{{child.name}}</span>
                            </bk-navigation-menu-item>
                        </div>
                    </bk-navigation-menu-item>
                </bk-navigation-menu>
            </template>
            <div class="monitor-navigation-content">
                <main class="main-content" v-bkloading="{ isLoading: mainContentLoading, opacity: 1 }">
                    <router-view :key="routerKey" v-show="!mainContentLoading" />
                </main>
            </div>
            <template slot="footer">
                <div class="monitor-navigation-footer">
                    Copyright © 2012-{{new Date().getFullYear()}} Tencent BlueKing. All Rights Reserved. 腾讯蓝鲸 版权所有
                </div>
            </template>
        </bk-navigation>
        <app-auth ref="bkAuth"></app-auth>
    </div>
</template>

<script>
    import { mapGetters } from 'vuex'

    import { bus } from '@/common/bus'

    export default {
        name: 'monitor-navigation',
        data () {
            return {
                routerKey: +new Date(),
                systemCls: 'mac',
                nav: {
                    list: [
                        {
                            id: 'home',
                            name: '首页',
                            icon: 'icon-home-shape',
                            pathName: 'home',
                            children: [],
                            group: true
                        },
                        {
                            id: '我的课程',
                            name: '我的课程',
                            icon: 'icon-tree-module-shape',
                            pathName: 'my_class',
                            children: [
                                {
                                    id: 'my_join_class',
                                    name: '我加入的课程',
                                    pathName: 'my_join_class'
                                },
                                {
                                    id: 'my_join_class_detail',
                                    name: '课程详情',
                                    pathName: 'my_join_class_detail'
                                },
                                {
                                    id: 'answer_question',
                                    name: '答题',
                                    pathName: 'answer_question'
                                }
                            ],
                            group: true
                        },
                        {
                            id: '课程管理',
                            name: '课程管理',
                            icon: 'icon-tree-process-shape',
                            pathName: 'class_manage',
                            children: [
                                {
                                    id: 'my_manage_class',
                                    name: '我管理的课程',
                                    pathName: 'my_manage_class'
                                },
                                {
                                    id: 'set_question',
                                    name: '我的出题',
                                    pathName: 'set_question'
                                }
                            ],
                            group: true
                        }
                    ],
                    id: 'home',
                    toggle: true,
                    submenuActive: false,
                    title: '蓝鲸测试平台'
                },
                header: {
                    list: [],
                    selectList: [],
                    active: 2,
                    bizId: 1
                },
                user: {
                    list: [
                        {
                            id: 'person',
                            name: '个人中心',
                            pathName: 'person'
                        },
                        {
                            id: 'exit',
                            name: '退出',
                            pathName: 'exit'
                        }
                    ]
                }
            }
        },
        computed: {
            ...mapGetters(['mainContentLoading']),
            curHeaderNav () {
                return this.header.list[this.header.active] || {}
            }
        },
        created () {
            const platform = window.navigator.platform.toLowerCase()
            if (platform.indexOf('win') === 0) {
                this.systemCls = 'win'
            }
        },
        mounted () {
            const self = this
            bus.$on('show-login-modal', data => {
                self.$refs.bkAuth.showLoginModal(data)
            })
            bus.$on('close-login-modal', () => {
                self.$refs.bkAuth.hideLoginModal()
                setTimeout(() => {
                    window.location.reload()
                }, 0)
            })
        },
        methods: {
            handleSelect (id, item) {
                this.nav.id = id
                console.info(`你选择了${id}`)
                this.$router.push({
                    name: item.pathName
                })
            },
            handleToggle (v) {
                this.nav.toggle = v
            }
        }
    }
</script>

<style lang="postcss">
    @import './css/reset.css';
    @import './css/app.css';

    .monitor-navigation-header {
        -webkit-box-flex: 1;
        -ms-flex: 1;
        flex: 1;
        overflow: hidden;
        height: 100%;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        font-size: 14px;
        .header-nav {
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            padding: 0;
            margin: 0;
        }
        .header-nav-item {
            list-style: none;
            height: 50px;
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            -webkit-box-align: center;
            -ms-flex-align: center;
            align-items: center;
            margin-right: 40px;
            color: #96A2B9;
            min-width: 56px;
            &.item-active {
                color: #fff !important;
            }
            &:hover {
                cursor: pointer;
                color: #d3d9e4;
            }
        }
        .header-title {
            color: #63656E;
            font-size: 16px;
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            -webkit-box-align: center;
            -ms-flex-align: center;
            align-items: center;
            margin-left: -6px;
        }
        .header-title-icon {
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            -webkit-box-align: center;
            -ms-flex-align: center;
            align-items: center;
            width: 28px;
            height: 28px;
            font-size: 28px;
            color: #3a84ff;
            cursor: pointer;
        }
        .header-select {
            width: 240px;
            margin-left: auto;
            margin-right: 34px;
            border: none;
            background: #252f43;
            color: #d3d9e4;
            -webkit-box-shadow: none;
            box-shadow: none;
        }
        .header-mind {
            color: #768197;
            font-size: 16px;
            position: relative;
            height: 32px;
            width: 32px;
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            -webkit-box-align: center;
            -ms-flex-align: center;
            align-items: center;
            -webkit-box-pack: center;
            -ms-flex-pack: center;
            justify-content: center;
            margin-right: 8px;
            &:hover {
                background: -webkit-gradient(linear,right top, left top,from(rgba(37,48,71,1)),to(rgba(38,50,71,1)));
                background: linear-gradient(270deg,rgba(37,48,71,1) 0%,rgba(38,50,71,1) 100%);
                border-radius: 100%;
                cursor: pointer;
                color: #d3d9e4;
            }
        }
        .header-mind-mark {
            position: absolute;
            right: 8px;
            top: 8px;
            height: 7px;
            width: 7px;
            border: 1px solid #27334C;
            background-color: #EA3636;
            border-radius: 100%
        }
        .header-user {
            height: 100%;
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            -webkit-box-align: center;
            -ms-flex-align: center;
            align-items: center;
            -webkit-box-pack: center;
            -ms-flex-pack: center;
            justify-content: center;
            color: #96A2B9;
            margin-left: 8px;
            &:hover {
                cursor: pointer;
                color: #d3d9e4;
            }
            .bk-icon {
                margin-left: 5px;
                font-size: 12px;
            }
        }
    }
    .monitor-navigation-content {
        padding: 5px 15px 15px 15px;
        font-size: 14px;
        color: #737987;
        height: calc(100% - 84px);
        background: #FFFFFF;
        -webkit-box-shadow: 0px 2px 4px 0px rgba(25,25,41,0.05);
        box-shadow: 0px 2px 4px 0px rgba(25,25,41,0.05);
        border-radius: 2px;
        border: 1px solid rgba(220,222,229,1);
        .main-content {
            min-height: 600px;
        }
    }
    .monitor-navigation-footer {
        height: 52px;
        width: 100%;
        margin: 32px 0 0;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        -webkit-box-pack: center;
        -ms-flex-pack: center;
        justify-content: center;
        border-top: 1px solid #dcdee5;
        color: #63656e;
        font-size: 12px;
    }
    .monitor-navigation-nav {
        width: 150px;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-orient: vertical;
        -webkit-box-direction: normal;
        -ms-flex-direction: column;
        flex-direction: column;
        background: #FFFFFF;
        border: 1px solid #E2E2E2;
        -webkit-box-shadow: 0px 3px 4px 0px rgba(64,112,203,0.06);
        box-shadow: 0px 3px 4px 0px rgba(64,112,203,0.06);
        padding: 6px 0;
        margin: 0;
        color: #63656E;
        .nav-item {
            -webkit-box-flex: 0;
            -ms-flex: 0 0 32px;
            flex: 0 0 32px;
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            -webkit-box-align: center;
            -ms-flex-align: center;
            align-items: center;
            padding: 0 16px;
            list-style: none;
            &:hover {
                color: #3A84FF;
                cursor: pointer;
                background-color: #F0F1F5;
            }
            .lang-icon {
                font-size: 20px;
                margin-right: 6px;
            }
        }
    }
    .monitor-navigation-admin {
        width: 170px #63656E;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-orient: vertical;
        -webkit-box-direction: normal;
        -ms-flex-direction: column;
        flex-direction: column;
        background: #FFFFFF;
        border: 1px solid #E2E2E2;
        -webkit-box-shadow: 0px 3px 4px 0px rgba(64,112,203,0.06);
        box-shadow: 0px 3px 4px 0px rgba(64,112,203,0.06);
        padding: 6px 0;
        margin: 0;
        color: #63656E;
        .nav-item {
            -webkit-box-flex: 0;
            -ms-flex: 0 0 32px;
            flex: 0 0 32px;
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            -webkit-box-align: center;
            -ms-flex-align: center;
            align-items: center;
            padding: 0 16px;
            list-style: none;
            &:hover {
                color: #3A84FF;
                cursor: pointer;
                background-color: #F0F1F5;
            }
            .lang-icon {
                font-size: 20px;
                margin-right: 6px;
            }
        }
    }
    .tippy-popper .tippy-tooltip.navigation-message-theme {
        padding: 0;
        border-radius: 0;
        -webkit-box-shadow: none;
        box-shadow: none;
    }
</style>
