<template>
    <div class="wrapper">
        <div>
            <bk-tab :active.sync="active" type="unborder-card">
                <!-- 为了保持数据同步，使用v-if销毁组件 -->
                <bk-tab-panel v-bind="{ name: 'userlist', label: '项目成员列表' }">
                    <div id="userlist">
                        <div class="topTab">
                            <bk-button
                                theme="primary" style="background: #88a2ef" @click="visible.deletebatch.isshow = true"
                                :disabled="user_id_list.length === 0">批量删除用户
                            </bk-button>
                            <div class="tabRight">
                                <bk-input
                                    left-icon="bk-icon icon-search"
                                    placeholder="搜索用户"
                                    v-model="search.name1"
                                    @blur="getProjectUser()"
                                    @keyup.enter.native="getProjectUser()"
                                    style="width: 300px; height: 32px">
                                </bk-input>
                            </div>
                        </div>
                        <!-- 表格本体 -->
                        <bk-table
                            :data="projectUserList"
                            :row-key="(row) => {
                                return row.id;
                            }"
                            :pagination="pagingConfigOne"
                            size="small"
                            height="62vh"
                            style="margin-top: 10px"
                            auto-scroll-to-top
                            @page-change="pageOneChange"
                            @selection-change="handleSelectDelete"
                            @page-limit-change="limitOneChange">
                            <bk-table-column type="selection" width="60" resizable></bk-table-column>
                            <bk-table-column
                                label="用户名"
                                column-key="username"
                                prop="username">
                            </bk-table-column>
                            <bk-table-column
                                label="姓名"
                                column-key="name"
                                prop="name">
                            </bk-table-column>
                            <!--                            <bk-table-column-->
                            <!--                                label="性别"-->
                            <!--                                column-key="gender"-->
                            <!--                                prop="gender"-->
                            <!--                                :filters="filters.gender"-->
                            <!--                                :filter-multiple="false"-->
                            <!--                                :width="100">-->
                            <!--                                <template slot-scope="props">{{-->
                            <!--                                    props.row.gender === "FEMALE"-->
                            <!--                                        ? "女"-->
                            <!--                                        : props.row.gender === "MALE"-->
                            <!--                                            ? "男"-->
                            <!--                                            : "未知"-->
                            <!--                                }}-->
                            <!--                                </template>-->
                            <!--                            </bk-table-column>-->
                            <bk-table-column
                                label="邮箱"
                                column-key="email"
                                prop="email"
                                align="center">
                            </bk-table-column>
                            <bk-table-column
                                label="标签"
                                column-key="tag"
                                prop="tag"
                                align="center">
                                <template slot-scope="props">
                                    <bk-tag
                                        v-for="tag in props.row.tag"
                                        :key="tag.tag_id"
                                        :style="'background-color:' + colorTransform(tag.tag_color)"
                                    >{{ tag.tag_value }}
                                    </bk-tag>
                                </template>
                            </bk-table-column>
                            <bk-table-column
                                label="最近登陆时间"
                                column-key="last_login"
                                prop="last_login"
                                :filters="filters.min_date"
                                :filter-multiple="false">
                            </bk-table-column>
                            <bk-table-column label="用户操作">
                                <template slot-scope="props">
                                    <bk-button theme="primary" text @click="openDeleteUserDialoag(props.row)">删除
                                    </bk-button>
                                </template>
                            </bk-table-column>
                        </bk-table>
                    </div>
                </bk-tab-panel>
                <bk-tab-panel v-bind="{ name: 'accounts', label: '导入项目成员' }">
                    <div id="importUser">
                        <div class="topTab">
                            <bk-button
                                theme="primary" style="background: #88a2ef"
                                @click="visible.importbatch.isshow = true"
                                :disabled="user_id_list.length === 0">批量导入选中用户
                            </bk-button>
                            <div class="tabRight">
                                <bk-input
                                    left-icon="bk-icon icon-search"
                                    placeholder="搜索用户"
                                    v-model="search.name2"
                                    @blur="getAllUserlist()"
                                    @keyup.enter.native="getAllUserlist()"
                                    style="width: 300px; height: 32px">
                                </bk-input>
                            </div>
                        </div>
                        <!-- 表格 -->
                        <bk-table
                            :data="userlist"
                            :row-key="
                                (row) => {
                                    return row.id;
                                }
                            "
                            :pagination="pagingConfigTwo"
                            size="small"
                            height="62vh"
                            style="margin-top: 10px"
                            auto-scroll-to-top
                            @page-change="pageTwoChange"
                            @selection-change="handleSelectImport"
                            @page-limit-change="limitTwoChange">
                            <bk-table-column type="selection" resizable></bk-table-column>
                            <bk-table-column
                                label="用户名"
                                column-key="username"
                                prop="username">
                            </bk-table-column>
                            <bk-table-column
                                label="姓名"
                                column-key="name"
                                prop="name">
                            </bk-table-column>
                            <!--                            <bk-table-column-->
                            <!--                                label="性别"-->
                            <!--                                column-key="gender"-->
                            <!--                                prop="gender"-->
                            <!--                                :filters="filters.gender"-->
                            <!--                                :filter-multiple="false">-->
                            <!--                                <template slot-scope="props">{{-->
                            <!--                                    props.row.gender === "FEMALE"-->
                            <!--                                        ? "女"-->
                            <!--                                        : props.row.gender === "MALE"-->
                            <!--                                            ? "男"-->
                            <!--                                            : "未知"-->
                            <!--                                }}-->
                            <!--                                </template>-->
                            <!--                            </bk-table-column>-->
                            <bk-table-column
                                label="邮箱"
                                column-key="email"
                                prop="email"
                                align="center"></bk-table-column>
                            <bk-table-column
                                label="标签"
                                column-key="tag"
                                prop="tag"
                                align="center">
                                <template slot-scope="props">
                                    <bk-tag
                                        v-for="tag in props.row.tag"
                                        :key="tag.tag_id"
                                        :style="'background-color:' + colorTransform(tag.tag_color)">{{ tag.tag_value }}
                                    </bk-tag>
                                </template>
                            </bk-table-column>
                            <bk-table-column
                                label="最近登陆时间"
                                column-key="last_login"
                                prop="last_login"
                                :filters="filters.min_date"
                                :filter-multiple="false">
                            </bk-table-column>
                            <bk-table-column label="操作" width="100">
                                <template slot-scope="props">
                                    <bk-button theme="primary" text @click="importToProject(props.row)"
                                        :disabled="props.row.disabledFlag">导入该用户
                                    </bk-button>
                                </template>
                            </bk-table-column>
                        </bk-table>
                    </div>
                </bk-tab-panel>
            </bk-tab>
        </div>
        <div>
            <!-- 删除用户 -->
            <bk-dialog v-model="visible.deleteuser.isshow"
                width="530"
                position="'top'"
                :mask-close="false"
                :header-position="visible.deleteuser.headerPosition"
                :title="'删除成员'"
                @confirm="removeUser(id)">
                <div class="dialog-body">
                    <h3>确定要将
                        <bk-tag>{{ item.name }}</bk-tag>
                        用户从项目成员中移除吗？
                    </h3>
                </div>
            </bk-dialog>
            <!-- 批量删除 -->
            <bk-dialog v-model="visible.deletebatch.isshow"
                width="530"
                position="'top'"
                :mask-close="false"
                :title="批量删除"
                :header-position="visible.deletebatch.headerPosition"
                @confirm="removeUser(id)">
                <div class="dialog-body">
                    <h3>确定要删除
                        <bk-tag>{{ user_id_list.length }}</bk-tag>
                        个用户吗？
                    </h3>
                </div>
            </bk-dialog>
            <!-- 批量导入 -->
            <bk-dialog v-model="visible.importbatch.isshow"
                width="530"
                position="'top'"
                :mask-close="false"
                :title="批量导入用户"
                :header-position="visible.importbatch.headerPosition"
                @confirm="importBatch">
                <div class="dialog-body">
                    <h3>确定要将这
                        <bk-tag>{{ user_id_list.length }}</bk-tag>
                        项用户批量导入到项目中吗？
                    </h3>
                </div>
            </bk-dialog>
        </div>
    </div>
</template>

<script>
    import { colorTransform } from '@/common/util'

    export default {
        name: 'course_number',
        data () {
            const current = new Date().getTime()
            return {
                active: 'userlist',
                course_id: '',
                // 列表
                memberList: '',
                // 搜索条件
                search: {
                    name1: '',
                    name2: '',
                    gender: '',
                    min_date: '',
                    max_date: '',
                    role: ''
                },
                // 用户列表
                userlist: [],
                user_id_list: [],
                // 项目成员列表
                projectUserList: [],
                // 新建用户
                importUserFlag: false,
                // 修改用户
                editUserFlag: false,
                userConfigCache: {},
                item: '',
                // 筛选
                filters: {
                    gender: [
                        { text: '男性', value: 'MALE' },
                        { text: '女性', value: 'FEMALE' }
                    ],
                    min_date: [
                        {
                            text: '近一星期',
                            value: new Date(current - 7 * 24 * 3600 * 1000).toLocaleString()
                        },
                        {
                            text: '近一月',
                            value: new Date(current - 30 * 24 * 3600 * 1000).toLocaleString()
                        },
                        {
                            text: '近一年',
                            value: new Date(current - 365 * 24 * 3600 * 1000).toLocaleString()
                        }
                    ]
                },
                // 导入
                importUser: {
                    visible: false
                },
                // 分页
                pagingConfigOne: {
                    current: 1,
                    limit: 10,
                    count: 0,
                    showLimit: true,
                    limitList: [5, 10, 20, 30]
                },
                pagingConfigTwo: {
                    current: 1,
                    limit: 10,
                    count: 0,
                    showLimit: true,
                    limitList: [5, 10, 20, 30]
                },
                // 关键字
                keyWord: '',
                disabledFlag: false,
                visible: { // 这是对话框的显示控制
                    deleteuser: {
                        isshow: false,
                        headerPosition: 'center'
                    },
                    deletebatch: {
                        isshow: false,
                        headerPosition: 'center'
                    },
                    importbatch: {
                        isshow: false,
                        headerPosition: 'Center'
                    }
                }
            }
        },
        watch: {
            // 监听当前课程id的变化
            '$store.state.currentCourseId' (newValue) {
                this.course_id = this.$store.state.currentCourseId
                this.getAllUserlist()
                this.getProjectUser()
            }
        },
        created () {
            this.course_id = this.$store.state.currentCourseId
        },
        mounted () {
            this.getAllUserlist()
            this.getProjectUser()
        },
        methods: {
            // 获取系统所有用户
            async getAllUserlist () {
                this.userlist = []
                this.$http.get(`api/users/`, {
                    params: {
                        page: this.pagingConfigTwo.current,
                        page_size: this.pagingConfigTwo.limit,
                        gender: this.search.gender,
                        name: this.search.name2,
                        min_date: this.search.last_login
                    }
                }).then((res) => {
                    this.pagingConfigTwo.count = res.data.count
                    this.userlist = res.data.results.map((item) => {
                        if (item.last_login === null) {
                            item.last_login = '用户最近暂未登录'
                        } else {
                            item.last_login = this.msToDate(item.last_login).hasTime
                        }
                        return item
                    })
                    this.isImport()
                })
            },
            // 时间格式化
            msToDate (msec) {
                const datetime = new Date(msec)
                const year = datetime.getFullYear()
                const month = datetime.getMonth()
                const date = datetime.getDate()
                const hour = datetime.getHours()
                const minute = datetime.getMinutes()
                const second = datetime.getSeconds()
                const result1 = year
                    + '-'
                    + ((month + 1) >= 10 ? (month + 1) : '0' + (month + 1))
                    + '-'
                    + ((date + 1) < 10 ? '0' + date : date)
                    + ' '
                    + ((hour + 1) < 10 ? '0' + hour : hour)
                    + ':'
                    + ((minute + 1) < 10 ? '0' + minute : minute)
                    + ':'
                    + ((second + 1) < 10 ? '0' + second : second)

                const result2 = year
                    + '-'
                    + ((month + 1) >= 10 ? (month + 1) : '0' + (month + 1))
                    + '-'
                    + ((date + 1) < 10 ? '0' + date : date)

                const result = {
                    hasTime: result1,
                    withoutTime: result2
                }
                return result
            },
            // 获取项目成员
            getProjectUser () {
                this.projectUserList = []
                this.$http.get(`api/project-user/${this.course_id}/`, {
                    params: {
                        page: this.pagingConfigOne.current,
                        page_size: this.pagingConfigOne.limit,
                        gender: this.search.gender,
                        name: this.search.name1,
                        min_date: this.search.last_login
                    }
                }).then((res) => {
                    this.pagingConfigOne.count = res.data.count
                    this.projectUserList = res.data.results.map((item) => {
                        if (item.last_login === null) {
                            item.last_login = '用户最近暂未登录'
                        } else {
                            item.last_login = this.msToDate(item.last_login).hasTime
                        }
                        return item
                    })
                })
            },
            // 导入单个用户
            importToProject (e) {
                this.$http.post('/api/project-user/', {
                    'project_id': this.course_id,
                    'user_id': JSON.stringify(e.id)
                }).then(res => {
                    if (res.result) {
                        this.$bkMessage({
                            message: '导入成功',
                            delay: 1000,
                            theme: 'success',
                            offsetY: 60,
                            ellipsisLine: 2
                        })
                    } else {
                        this.$bkMessage({
                            message: '导入失败，请重试',
                            delay: 1000,
                            theme: 'error',
                            offsetY: 60,
                            ellipsisLine: 2
                        })
                    }
                })
            },
            // 批量导入
            importBatch () {
                this.$http.post(`/api/project-user/${this.course_id}/`, { 'user_id_list': this.user_id_list }).then(res => {
                    if (res.result) {
                        this.$bkMessage({
                            message: '导入成功',
                            delay: 1000,
                            theme: 'success',
                            offsetY: 60,
                            ellipsisLine: 2
                        })
                        this.user_id_list = ''
                        this.getProjectUser()
                    } else {
                        this.$bkMessage({
                            message: '导入失败，请重试',
                            delay: 1000,
                            theme: 'error',
                            offsetY: 60,
                            ellipsisLine: 2
                        })
                    }
                    this.getProjectUser()
                })
            },
            openDeleteUserDialoag (e) {
                this.user_id_list = []
                this.user_id_list.push(e.id)
                this.item = e
                this.visible.deleteuser.isshow = true
            },

            removeUser (e) {
                this.$http.delete(`/api/project-user/${this.course_id}/`, { data: { 'user_id_list': this.user_id_list } }).then(res => {
                    if (res.result) {
                        this.$bkMessage({
                            message: '删除成功',
                            delay: 1000,
                            theme: 'success',
                            offsetY: 60,
                            ellipsisLine: 2
                        })
                        this.getProjectUser()
                    } else {
                        this.$bkMessage({
                            message: '删除失败',
                            delay: 1000,
                            theme: 'error',
                            offsetY: 60,
                            ellipsisLine: 2
                        })
                        this.getProjectUser()
                    }
                })
                this.getProjectUser()
                this.user_id_list = []
            },
            // 删除多项
            handleSelectDelete (selection) {
                this.user_id_list = []
                selection.forEach(e => {
                    this.user_id_list.push(e.id)
                })
            },
            // 导入多项
            handleSelectImport (selection) {
                this.user_id_list = []
                selection.forEach(e => {
                    this.user_id_list.push(e.id)
                })
            },
            // 分页一
            pageOneChange (page) {
                this.pagingConfigOne.current = page
                this.getProjectUser()
            },
            // 页码的限制发生改变一
            limitOneChange (limit) {
                this.pagingConfigOne.limit = limit
                this.getProjectUser()
            },
            // 分页二
            pageTwoChange (page) {
                this.pagingConfigTwo.current = page
                this.getAllUserlist()
            },
            // 页码的限制发生改变二
            limitTwoChange (limit) {
                this.pagingConfigTwo.limit = limit
                this.getAllUserlist()
            },
            // 判断该用户是否被导入
            isImport () {
                for (const item of this.userlist) {
                    const itemId = item.id
                    const someResult = this.projectUserList.some(function (e) {
                        return e.id === itemId
                    })
                    if (someResult === true || someResult === 'true') {
                        item.disabledFlag = true
                    } else if (someResult === false || someResult === 'false') {
                        item.disabledFlag = false
                    }
                }
            },
            colorTransform
        }
    }
</script>

<style scoped>
@import './course_number.css';

/*项目成员列表部分css*/
#tab {
    display: flex;
    justify-content: space-between;
    margin-bottom: 5px;
    margin-top: 1px;

}

#batch {
    display: flex;
    justify-content: space-between;
}

.bk-dropdown-menu {
    padding: 8px 14px;
    background: #3a84ff;
    border-color: #3a84ff;
    color: #fff;
}

span {
    font-size: 14px;
    font-weight: 800;
}

.tabRight {
    display: flex;
    flex-direction: row;
    height: 32px;
}

.tabRight .bk-input {
    height: 32px !important;
}

/*导入项目成员部分css*/
.topTab {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    margin-top: 5px;
    margin-bottom: 5px;
}
</style>
