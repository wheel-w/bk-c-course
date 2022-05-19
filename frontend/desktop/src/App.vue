<template>
    <div
        class="monitor-navigation"
        :class="systemCls"
        v-title
        data-title="课程管理系统">
        <bk-navigation
            :header-title="nav.id"
            :side-title="nav.title"
            :default-open="true"
            :navigation-type="'left-right'"
            :theme-color="'#7090D9'"
            :need-menu="true">
            <template slot="header">
                <div class="monitor-navigation-header">
                    <div class="header-select">
                        <bk-select
                            v-if="
                                nav.id !== 'home' &&
                                    nav.id !== 'person' &&
                                    nav.id !== 'mycourse' &&
                                    nav.id !== 'exit'
                            "
                            v-model="$store.state.currentCourseId"
                            style="width: 250px"
                            ext-cls="select-custom"
                            ext-popover-cls="select-popover-custom"
                            searchable
                            :disabled="false">
                            <bk-option
                                v-for="option in courseList"
                                :key="option.id"
                                :id="option.id"
                                :name="option.name">
                            </bk-option>
                        </bk-select>
                    </div>
                    <bk-popover
                        theme="light navigation-message"
                        :arrow="false"
                        offset="-20, 10"
                        placement="bottom-start"
                        :tippy-options="{ hideOnClick: false }">
                        <div class="header-user">
                            {{ $store.state.user.username }}
                            <i class="bk-icon icon-down-shape"></i>
                        </div>
                        <template slot="content">
                            <ul class="monitor-navigation-admin">
                                <li
                                    class="nav-item"
                                    v-for="userItem in user.list"
                                    :key="userItem"
                                    @click="handleSelect(userItem.id, userItem)">
                                    {{ userItem.name }}
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
                    icon="circle"
                    :default-active="nav.pathName"
                    :item-default-bg-color="'#7690D9'"
                    :item-hover-bg-color="'#5E7AC5'"
                    :item-active-bg-color="'#5E7AC5'"
                    :item-default-color="'#f6f6f6'"
                    :item-hover-color="'#8ae4f5'"
                    :item-active-color="'#fea3be'"
                    :toggle-active="nav.toggle">
                    <bk-navigation-menu-item
                        v-for="item in nav.list"
                        :has-child="item.children.length === 0 ? false : true"
                        :key="item.pathName"
                        :default-active="item.active"
                        v-bind="item">
                        <!-- 图标 -->
                        <bk-icon
                            type="circle-shape"
                            :style="`color: ${item.color}`" />
                        <span style="margin-left: 20px">{{ item.name }}</span>
                        <div slot="child">
                            <bk-navigation-menu-item
                                v-for="child in item.children"
                                :key="child.id"
                                v-bind="child">
                                <span>{{ child.name }}</span>
                            </bk-navigation-menu-item>
                        </div>
                    </bk-navigation-menu-item>
                </bk-navigation-menu>
            </template>
            <div class="monitor-navigation-content" id="a">
                <main
                    class="main-content"
                    v-bkloading="{ isLoading: mainContentLoading, opacity: 1 }">
                    <router-view :key="routerKey" v-show="!mainContentLoading" />
                </main>
            </div>
            <template slot="footer">
                <div class="monitor-navigation-footer">
                    Copyright © 2012-{{ new Date().getFullYear() }} Tencent BlueKing. All
                    Rights Reserved. 腾讯蓝鲸 版权所有
                </div>
            </template>
        </bk-navigation>
        <bk-dialog
            v-model="register.primary.visible"
            theme="primary"
            :mask-close="false"
            ok-text="去认证"
            :confirm-fn="toRegister"
            :header-position="register.primary.headerPosition"
            title="去认证">
            您还没有进行身份认证，点击去认证按钮即可跳转至认证页面。
        </bk-dialog>
        <app-auth ref="bkAuth"></app-auth>
    </div>
</template>

<script>
    import { mapGetters } from 'vuex'

    import { bus } from '@/common/bus'
    import { bkDialog } from 'bk-magic-vue'

    export default {
        name: 'monitor-navigation',
        components: {
            bkDialog
        },
        data () {
            return {
                register: {
                    primary: {
                        visible: false,
                        headerPosition: 'left'
                    }
                },
                routerKey: +new Date(),
                systemCls: 'mac',
                nav: {
                    list: [
                        {
                            name: '首页',
                            pathName: 'home',
                            color: '#66ccff',
                            children: [],
                            group: true
                        },
                        {
                            name: '项目管理',
                            pathName: 'my_course',
                            color: '#b1de4f',
                            children: [],
                            group: true
                        },
                        {
                            name: '项目成员',
                            pathName: 'course_number',
                            color: '#fea3be',
                            children: [],
                            group: true
                        },
                        {
                            name: '任务题库',
                            pathName: 'set_question_index',
                            children: [],
                            color: '#fe33be',
                            group: true
                        },
                        {
                            name: '测验与作业',
                            color: '#fe8b5e',
                            children: [],
                            group: true
                        },
                        {
                            name: '任务管理',
                            pathName: 'displaypaper',
                            color: '#66ccff',
                            children: [],
                            group: true
                        },
                        {
                            name: '用户管理',
                            pathName: 'user_manage',
                            color: '#3399FF',
                            children: [],
                            group: true
                        },
                        {
                            name: '出题',
                            pathName: 'set_question',
                            color: '#33FF99',
                            children: [],
                            group: true
                        },
                        {
                            name: 'tag管理',
                            pathName: 'tag_manage',
                            color: '#dd75ca',
                            children: [],
                            group: true
                        }
                    ],
                    pathName: window.location.pathname.split('/').pop(),
                    toggle: true,
                    submenuActive: false,
                    title: '课程管理系统'
                },
                // 这里navTeacher和navStudent我没改，有需要的话从上面复制一下就可以
                navTeacher: {
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
                            id: 'mycourse',
                            name: '我的课程',
                            icon: 'icon-tree-module-shape',
                            pathName: 'my_course',
                            children: [],
                            group: true
                        },
                        {
                            id: 'classnumber',
                            name: '课程成员',
                            icon: 'icon-tree-module-shape',
                            pathName: 'course_number',
                            children: [],
                            group: true
                        },
                        {
                            id: 'set_question_index',
                            name: '课程题库',
                            icon: 'icon-tree-process-shape',
                            pathName: 'set_question_index',
                            children: [],
                            group: true
                        },
                        {
                            id: 'answer_question_index',
                            name: '测验与作业',
                            icon: 'icon-tree-process-shape',
                            pathName: 'answer_question_index',
                            children: [],
                            group: true
                        },
                        {
                            id: 'displaypaper',
                            name: '作业管理',
                            icon: 'icon-tree-process-shape',
                            pathName: 'displaypaper',
                            children: [],
                            group: true
                        },
                        {
                            id: 'user_manage',
                            name: '用户管理',
                            pathName: 'user_manage',
                            children: [],
                            group: true
                        }
                    ],
                    id: 'home',
                    toggle: true,
                    submenuActive: false,
                    title: '课程管理系统'
                },
                navStudent: {
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
                            id: 'mycourse',
                            name: '我的课程',
                            icon: 'icon-tree-module-shape',
                            pathName: 'my_course',
                            children: [],
                            group: true
                        },
                        {
                            id: 'classnumber',
                            name: '课程成员',
                            icon: 'icon-tree-module-shape',
                            pathName: 'course_number',
                            children: [],
                            group: true
                        },
                        {
                            id: 'answer_question_index',
                            name: '答题页面',
                            icon: 'icon-tree-process-shape',
                            pathName: 'answer_question_index',
                            children: [],
                            group: true
                        }
                    ],
                    id: 'home',
                    toggle: true,
                    submenuActive: false,
                    title: '课程管理系统'
                },
                navNotCertified: {
                    list: [
                        {
                            id: 'home',
                            name: '首页',
                            icon: 'icon-home-shape',
                            pathName: 'home',
                            children: [],
                            group: true
                        }
                    ],
                    id: 'home',
                    toggle: true,
                    submenuActive: false,
                    title: '课程管理系统'
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
                },
                courseList: []
            }
        },
        computed: {
    ...mapGetters(['mainContentLoading']),
    curHeaderNav () {
      return this.header.list[this.header.active] || {}
    }
        },
        created () {
            // this.getUserInfo()
            if (sessionStorage.getItem('courseId')) {
                this.$store.commit(
                    'updateCourseId',
                    JSON.parse(sessionStorage.getItem('courseId'))
                )
            }
            // 在页面刷新时将信息保存到sessionStorage里
            window.addEventListener('beforeunload', () => {
                sessionStorage.setItem('navId', JSON.stringify(this.nav.id))
                sessionStorage.setItem(
                    'courseId',
                    JSON.stringify(this.$store.state.currentCourseId)
                )
            })

            this.getCourseList()
            const platform = window.navigator.platform.toLowerCase()
            if (platform.indexOf('win') === 0) {
                this.systemCls = 'win'
            }
        },
        mounted () {
            const self = this
            bus.$on('show-login-modal', (data) => {
                self.$refs.bkAuth.showLoginModal(data)
            })
            bus.$on('close-login-modal', () => {
                self.$refs.bkAuth.hideLoginModal()
                setTimeout(() => {
                    window.location.reload()
                }, 0)
            })
            // 更新当前导航栏状态
            bus.$on('updateNavId', (id) => {
                self.nav.id = id
            })
            // 其他页面更新课程下拉选框
            bus.$on('updateCourseList', () => {
                self.getCourseList()
            })
        },
        methods: {
            // 点击导航栏跳转对应页面
            handleSelect (id, item) {
                this.nav.id = id
                if (item.pathName === 'exit') {
                    const HOST = `${window.location.protocol}//${window.location.host}`
                    const SITE_URL = window.PROJECT_CONFIG.SITE_URL
                    const BK_PAAS_HOST = window.PROJECT_CONFIG.BK_PAAS_HOST
                    const APP_CODE = window.PROJECT_CONFIG.APP_CODE
                    let path = `${SITE_URL}/&app_code=${APP_CODE}`
                    path = path.replace(new RegExp('/+', 'gm'), '/')
                    sessionStorage.removeItem('navId')
                    sessionStorage.removeItem('courseId')
                    this.nav.id = 'home'
                    this.$store.commit('updateCourseId', 0)
                    window.location.href = `${BK_PAAS_HOST}/login/?c_url=${HOST}${path}`
                }
                this.$router.push({
                    name: item.pathName
                })
            },
            // 获取课程列表
            async getCourseList () {
                this.$http.get('/api/project/').then((res) => {
                    if (res.data.results.length !== 0) {
                        this.courseList = res.data.results
                    }
                    if (this.$store.state.currentCourseId === 0) {
                        this.$store.commit('updateCourseId', res.data.results[0].id)
                    }
                })
            },
            async getUserInfo () {
                this.$http.get('/account/get_user_info/').then((res) => {
                    if (res.data.identity === 'TEACHER') {
                        this.nav = this.navTeacher
                    } else if (res.data.identity === 'STUDENT') {
                        this.nav = this.navStudent
                    } else if (res.data.identity === 'NOT_CERTIFIED') {
                        this.nav = this.navNotCertified
                        this.register.primary.visible = true
                    }
                    // 在页面加载时读取sessionStorage里的状态信息
                    this.nav.id = sessionStorage.getItem('navId')
                        ? JSON.parse(sessionStorage.getItem('navId'))
                        : 'home'
                })
            },
            toRegister () {
                this.$router.push({
                    name: 'person'
                })
                this.register.primary.visible = false
            }
        }
    }
</script>
<style lang="postcss">
@import "./css/reset.css";
@import "./css/app.css";
/*svg{*/
/*    color: #00c873 !important;*/
/*    width: 18px;*/
/*    height: 18px;*/
/*}*/
.bk-dialog-content {
  background-image: url("./images/add_dialog_bg.png");
}
.bk-dialog-footer {
  background-color: #cbd2e6 !important;
}
.monitor-navigation-header {
  -webkit-box-flex: 1;
  -ms-flex: 1;
  flex: 1;
  overflow: hidden;
  height: 100%;
  width: 100%;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
  padding: 0;
  margin: 0;
  background-image: url("./images/header_bg.png");
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
    color: #96a2b9;
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
    color: #63656e;
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
      background: -webkit-gradient(
        linear,
        right top,
        left top,
        from(rgba(37, 48, 71, 1)),
        to(rgba(38, 50, 71, 1))
      );
      background: linear-gradient(
        270deg,
        rgba(37, 48, 71, 1) 0%,
        rgba(38, 50, 71, 1) 100%
      );
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
    border: 1px solid #27334c;
    background-color: #ea3636;
    border-radius: 100%;
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
    /*color: #96A2B9;*/
    color: #63656e;
    margin-left: 8px;
    margin-right: 30px;
    &:hover {
      cursor: pointer;
      color: #000000;
    }
    .bk-icon {
      margin-left: 5px;
      font-size: 12px;
    }
  }
}
&:hover {
  cursor: pointer;
  color: #d3d9e4;
}
.header-title {
  color: #63656e;
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
    background: -webkit-gradient(
      linear,
      right top,
      left top,
      from(rgba(37, 48, 71, 1)),
      to(rgba(38, 50, 71, 1))
    );
    background: linear-gradient(
      270deg,
      rgba(37, 48, 71, 1) 0%,
      rgba(38, 50, 71, 1) 100%
    );
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
  border: 1px solid #27334c;
  background-color: #ea3636;
  border-radius: 100%;
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
  /*color: #96A2B9;*/
  color: #63656e;
  margin-left: 8px;
  margin-right: 30px;
  &:hover {
    cursor: pointer;
    color: #000000;
  }
  .bk-icon {
    margin-left: 5px;
    font-size: 12px;
  }
}
.monitor-navigation-content {
  padding: 5px 15px 15px 15px;
  font-size: 14px;
  color: #737987;
  height: calc(100% - 84px);
  background: #ffffff;
  -webkit-box-shadow: 0px 2px 4px 0px rgba(25, 25, 41, 0.05);
  box-shadow: 0px 2px 4px 0px rgba(25, 25, 41, 0.05);
  border-radius: 2px;
  border: 1px solid rgba(220, 222, 229, 1);
  .main-content {
    height: 100%;
    .wrapper {
      height: 100%;
    }
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
  background: #ffffff;
  border: 1px solid #e2e2e2;
  -webkit-box-shadow: 0px 3px 4px 0px rgba(64, 112, 203, 0.06);
  box-shadow: 0px 3px 4px 0px rgba(64, 112, 203, 0.06);
  padding: 6px 0;
  margin: 0;
  color: #63656e;
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
      color: #3a84ff;
      cursor: pointer;
      background-color: #f0f1f5;
    }
    .lang-icon {
      font-size: 20px;
      margin-right: 6px;
    }
  }
}
.icon-circle-shape {
  font-size: 8px !important;
}
.monitor-navigation-admin {
  width: 250px #63656e;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-orient: vertical;
  -webkit-box-direction: normal;
  -ms-flex-direction: column;
  flex-direction: column;
  background: #ffffff;
  border: 1px solid #e2e2e2;
  -webkit-box-shadow: 0px 3px 4px 0px rgba(64, 112, 203, 0.06);
  box-shadow: 0px 3px 4px 0px rgba(64, 112, 203, 0.06);
  padding: 6px 0;
  margin: 0;
  color: #63656e;
  .nav-item {
    -webkit-box-flex: 0 0 30px;
    -ms-flex: 0 0 55px;
    flex: 0 0 42px;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    padding: 0 30px;
    list-style: none;
    &:hover {
      color: #3a84ff;
      cursor: pointer;
      background-color: #f0f1f5;
    }
    .lang-icon {
      font-size: 40px;
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
.bk-navigation-wrapper .navigation-nav .nav-slider-footer .footer-icon.is-left {
  color: #f6f6f6 !important;
}
.bk-navigation-title {
  background-color: #5c7ac4;
}
.bk-navigation-title span {
  color: #ffffff !important;
}
.bk-navigator-title .title-desc {
  background-image: url("./images/header_bg.png");
}

.navigation-menu-item {
  background-color: #89a3ef;
  border-radius: 20px;
}
.navigation-menu {
  width: 85%;
  margin: 20px auto;
}
.container-header {
  padding: 0 !important;
}
.nav-slider {
  background-image: url("./images/nav_bg.png");
}
/* 删除原有title-icon */
/* 这里原本使用nexttick实现，我觉得很没必要，所以改了 */
span.title-icon > i {
  display: none;
}
</style>
