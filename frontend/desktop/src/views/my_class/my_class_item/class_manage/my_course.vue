<template>
    <div class="wrapper">
        <div class="wrapper-head" v-if="userIdentify === 'TEACHER'">
            <bk-button theme="primary" class="mr10" :outline="true" @click="beforeAdd">创建课程</bk-button>
            <bk-button theme="primary" :outline="true" @click="removeallBefore">批量删除</bk-button>
        </div>
        <div class="wrapper-body">
            <bk-table style="margin-top: 10px;"
                size="small"
                :data="List"
                :pagination="pagination"
                @selection-change="handleSelect"
                @row-mouse-enter="handleRowMouseEnter"
                @row-mouse-leave="handleRowMouseLeave"
                @page-change="handlePageChange"
                @page-limit-change="handlePageLimitChange">
                <bk-table-column v-if="userIdentify === 'TEACHER'" type="selection" width="60" align="center" header-align="center"></bk-table-column>
                <bk-table-column label="课程id" prop="course_id" align="center" header-align="center"></bk-table-column>
                <bk-table-column label="课程名称" prop="course_name" align="center" header-align="center"></bk-table-column>
                <bk-table-column label="任课老师" prop="teacher" align="center" header-align="center"></bk-table-column>
                <bk-table-column label="课程管理员" align="center" header-align="center">
                    <template slot-scope="props">
                        <bk-popover placement="top" v-if="props.row.manage_student.length !== 0">
                            <span>{{props.row.manage_student.toString().slice(0,12) + (props.row.manage_student.toString().length > 12 ? '...' : '')}}</span>
                            <div slot="content">
                                <div class="bk-text pt10 pb5 pl10 pr10" v-for="(item, index) in props.row.manage_student" :key="index">{{item}}</div>
                            </div>
                        </bk-popover>
                    </template>
                </bk-table-column>
                <bk-table-column label="创建人" prop="create_people" align="center" header-align="center"></bk-table-column>
                <bk-table-column label="课程简介" header-align="center" align="center">
                    <template slot-scope="props">
                        <bk-popover placement="top" v-if="props.row.course_introduction !== 0">
                            <span>{{props.row.course_introduction.slice(0,12) + (props.row.course_introduction.length > 12 ? '...' : '')}}</span>
                            <div slot="content">
                                <div class="bk-text pt10 pb5 pl10 pr10">{{props.row.course_introduction}}</div>
                            </div>
                        </bk-popover>
                    </template>
                </bk-table-column>
                <bk-table-column label="操作" width="150" align="center" header-align="center" v-if="userIdentify === 'TEACHER'">
                    <template slot-scope="props">
                        <bk-button class="mr10" theme="primary" text @click="alterBefore(props.row)">修改</bk-button>
                        <bk-button class="mr10" theme="primary" text @click="removeBefor(props.row)">删除</bk-button>
                    </template>
                </bk-table-column>
            </bk-table>
            <div style="padding-top: 10px;">
                <bk-pagination
                    size="small"
                    :current.sync="pagingConfigTwo.current"
                    :limit.sync="pagingConfigTwo.limit"
                    :count="pagingConfigTwo.count"
                    :location="pagingConfigTwo.location"
                    :align="pagingConfigTwo.align"
                    :show-limit="pagingConfigTwo.showLimit"
                    :limit-list="pagingConfigTwo.limitList"
                    :show-total-count="true"
                    @change="pageChange"
                    @limit-change="limitChange">
                </bk-pagination>
            </div>
        </div>
        <div id="dialoge">
            <!-- 创建课程的对话框 -->
            <bk-dialog v-model="visible.addcourse.isshow"
                width="530"
                position="'top'"
                :mask-close="false"
                :header-position="visible.addcourse.headerPosition"
                @confirm="addCourse"
                title="创建课程">
                <bk-form :model="formData" :rules="rules" ref="validateForm">
                    <bk-form-item
                        label="课程名称"
                        :required="true"
                        :property="'course_name'"
                        :error-display-type="'normal'">
                        <bk-input v-model="formData.course_name" style="width: 250px;" placeholder="请输入课程名称"></bk-input>
                    </bk-form-item>
                    <bk-form-item
                        label="任课老师"
                        :required="true"
                        :property="'teacher'"
                        :error-display-type="'normal'">
                        <bk-select :disabled="false" v-model="formData.teacher_id" style="width: 250px;"
                            ext-cls="select-custom"
                            ext-popover-cls="select-popover-custom"
                            searchable>
                            <bk-option v-for="option in teacherList"
                                :key="option.member_id"
                                :id="option.member_id"
                                :name="option.member_display_name">
                            </bk-option>
                        </bk-select>
                    </bk-form-item>
                    <bk-form-item label="课程管理员">
                        <bk-select :disabled="false" v-model="formData.manage_student_ids" style="width: 250px;"
                            multiple
                            display-tag
                            :auto-height="false"
                            ext-cls="select-custom"
                            ext-popover-cls="select-popover-custom"
                            searchable>
                            <bk-option v-for="option in studentList"
                                :key="option.member_id"
                                :id="option.member_id"
                                :name="option.member_display_name">
                            </bk-option>
                        </bk-select>
                    </bk-form-item>
                    <bk-form-item label="课程简介">
                        <bk-input type="textarea" style="width: 250px;" v-model="formData.course_introduction" placeholder="在这里输入课程简介"></bk-input>
                    </bk-form-item>
                </bk-form>
            </bk-dialog>
            <!-- 删除课程 -->
            <bk-dialog v-model="visible.deletcourse.isshow"
                width="530"
                position="'top'"
                :mask-close="false"
                :header-position="visible.addcourse.headerPosition"
                :title="'删除除课程'"
                @confirm="removeCourse(course_id)">
                <div class="dialog-body">
                    <p>确定要删除{{formData3.course_name}}这门课程吗</p>
                </div>
            </bk-dialog>
            <!-- 批量删除 -->
            <bk-dialog v-model="visible.deleteall.isshow"
                width="530"
                position="'top'"
                :mask-close="false"
                :header-position="visible.deleteall.headerPosition"
                @confirm="removeCourse(course_id)">
                <div class="dialog-body">
                    <p>确定要删除{{course_id.length}}项内容吗？</p>
                </div>
            </bk-dialog>
            <!-- 修改课程 -->
            <bk-dialog v-model="visible.altercourse.isshow"
                width="530"
                position="'top'"
                :mask-close="false"
                :header-position="visible.addcourse.headerPosition"
                @confirm="alterCourse">
                <bk-form :model="formData2" :rules="rules" ref="validateForm">
                    <bk-form-item
                        label="课程名称"
                        :required="true"
                        :property="'course_name'"
                        :error-display-type="'normal'">
                        <bk-input v-model="formData2.course_name" style="width: 250px;" placeholder="请输入课程名称"></bk-input>
                    </bk-form-item>
                    <bk-form-item
                        label="任课老师"
                        :required="true"
                        :property="'teacher'"
                        :error-display-type="'normal'">
                        <bk-select :disabled="false" v-model="formData2.teacher" style="width: 250px;"
                            ext-cls="select-custom"
                            ext-popover-cls="select-popover-custom"
                            searchable>
                            <bk-option v-for="option in teacherList"
                                :key="option.member_id"
                                :id="option.member_display_name"
                                :name="option.member_display_name">
                            </bk-option>
                        </bk-select>
                    </bk-form-item>
                    <bk-form-item label="学生管理员">
                        <bk-select :disabled="false" v-model="formData2.manage_student" style="width: 250px;"
                            multiple
                            display-tag
                            :auto-height="false"
                            ext-cls="select-custom"
                            ext-popover-cls="select-popover-custom"
                            searchable>
                            <bk-option v-for="option in studentList"
                                :key="option.member_id"
                                :id="option.member_display_name"
                                :name="option.member_display_name">
                            </bk-option>
                        </bk-select>
                    </bk-form-item>
                    <bk-form-item label="课程简介">
                        <bk-input type="textarea" style="width: 250px;" v-model="formData2.course_introduction" placeholder="在这里输入课程简介"></bk-input>
                    </bk-form-item>
                </bk-form>
            </bk-dialog>
        </div>
    </div>
</template>

<script>
    import { bus } from '@/common/bus'
    export default {
        data () {
            return {
                userIdentify: '',
                course: [],
                teacherList: [],
                studentList: [],
                course_id: [],
                List: [],
                formData: {
                    course_name: '',
                    teacher_id: '',
                    teacher: '',
                    manage_student_ids: [],
                    manage_student: [],
                    course_introduction: ''
                },
                formData2: {
                    id: '',
                    course_name: '',
                    teacher_id: '',
                    teacher: '',
                    manage_student_id: [],
                    manage_student: [],
                    course_introduction: ''
                },
                formData3: '',
                visible: { // 这是对话框的显示控制
                    addcourse: {
                        isshow: false,
                        headerPosition: 'center'
                    },
                    deletcourse: {
                        isshow: false,
                        headerPosition: 'center'
                    },
                    altercourse: {
                        isshow: false,
                        headerPosition: 'center'
                    },
                    deleteall: {
                        isshow: false,
                        headerPosition: 'center'
                    }
                },
                pagingConfigTwo: {
                    current: 1,
                    limit: 10,
                    count: 0,
                    location: 'left',
                    align: 'right',
                    showLimit: true,
                    limitList: [5, 10, 20, 30]
                }
            }
        },
        created () {
            this.getList()
            this.userIdentify = this.$store.state.user.identity
        },
        methods: {
            getList () {
                // 拿到课程信息
                this.$http.get('/course/find_courses/').then(res => {
                    if (res.result) {
                        this.course = res.data
                        this.pagingConfigTwo.count = this.course.length
                        const right = this.pagingConfigTwo.current * this.pagingConfigTwo.limit
                        const left = right - this.pagingConfigTwo.limit
                        this.List = this.course.slice(left, right)
                        bus.$emit('updateCourseList')
                    } else {
                        this.$bkMessage({
                            message: '页面加载出错，请刷新重试！',
                            delay: 1000,
                            theme: 'error',
                            offsetY: 60,
                            ellipsisLine: 2 })
                    }
                })
                // 拿到老师列表
                this.$http.get('/course/search_member_info/?member_identify=TEACHER').then(res => {
                    if (res.result) {
                        this.teacherList = res.data
                    } else {
                        this.$bkMessage({
                            message: '页面加载出错，请刷新重试！',
                            delay: 1000,
                            theme: 'error',
                            offsetY: 60,
                            ellipsisLine: 2 })
                    }
                })
                // 拿到所有学生列表
                this.$http.get('/course/search_member_info/?member_identify=STUDENT').then(res => {
                    if (res.result) {
                        this.studentList = res.data
                    } else {
                        this.$bkMessage({
                            message: '页面加载出错，请刷新重试！',
                            delay: 1000,
                            theme: 'error',
                            offsetY: 60,
                            ellipsisLine: 2 })
                    }
                })
            },
            // 增加课程
            beforeAdd () {
                this.studentList = this.studentList.concat(this.teacherList)
                this.visible.addcourse.isshow = true
            },
            addCourse () {
                if (this.formData.course_name === '' || this.formData.teacher_id === '') {
                    this.$bkMessage({
                        message: '请补全内容',
                        delay: 1000,
                        theme: 'error',
                        offsetY: 60,
                        ellipsisLine: 2 })
                    this.visible.addcourse.isshow = true
                } else {
                    const that = this
                    that.teacherList.forEach(e => {
                        if (e.member_id === that.formData.teacher_id) {
                            that.formData.teacher = e.member_display_name
                        }
                    })
                    const hh = that.studentList.filter(function (Value) {
                        const length = that.formData.manage_student_ids.length
                        for (let i = 0; i < length; i++) {
                            if (Value.member_id === that.formData.manage_student_ids[i]) {
                                return Value
                            }
                        }
                    })
                    hh.forEach(e => {
                        this.formData.manage_student.push(e.member_display_name)
                    })
                    this.$http.post('/course/manage_course/', this.formData).then(res => {
                        if (res.result) {
                            this.$bkMessage({
                                message: '创建成功',
                                delay: 1000,
                                theme: 'success',
                                offsetY: 60,
                                ellipsisLine: 2 })
                            this.$store.commit('updateCourseId', 0)
                            this.getList()
                            this.List = this.course.slice(0, this.pagingConfigTwo.limit)
                            this.formData.course_name = ''
                            this.formData.teacher_id = ''
                            this.formData.teacher = ''
                            this.formData.manage_student = []
                            this.formData.manage_student_ids = []
                            this.formData.course_introduction = ''
                        } else {
                            this.$bkMessage({
                                message: '创建失败，请重试',
                                delay: 1000,
                                theme: 'error',
                                offsetY: 60,
                                ellipsisLine: 2 })
                        }
                    })
                }
            },
            // 删除多项
            handleSelect (selection) {
                this.course_id = []
                selection.forEach(e => {
                    this.course_id.push(e.course_id)
                })
            },
            removeallBefore () {
                if (this.course_id.length !== 0) {
                    this.visible.deleteall.isshow = true
                }
            },
            // 删除单个课程
            removeBefor (e) {
                this.course_id = []
                this.formData3 = e
                this.course_id.push(e.course_id)
                this.visible.deletcourse.isshow = true
            },
            removeCourse (e) {
                this.$http.delete('/course/manage_course/', { params: { course_id: JSON.stringify(e) } }).then(res => {
                    if (res.result) {
                        this.$bkMessage({
                            message: res.message,
                            delay: 1000,
                            theme: 'success',
                            offsetY: 60,
                            ellipsisLine: 2 })
                        this.$store.commit('updateCourseId', 0)
                        this.getList()
                    } else {
                        this.$bkMessage({
                            message: res.message,
                            delay: 1000,
                            theme: 'error',
                            offsetY: 60,
                            ellipsisLine: 2 })
                    }
                })
                this.formData3 = ''
            },
            // 修改课程
            alterBefore (e) {
                this.formData2.manage_student = []
                this.studentList = this.studentList.concat(this.teacherList)
                this.formData2.id = e.course_id
                this.formData2.course_name = e.course_name
                this.formData2.course_introduction = e.course_introduction
                this.formData2.manage_student = e.manage_student
                this.formData2.teacher = e.teacher
                this.formData2.manage_student_id.length = 0
                this.visible.altercourse.isshow = true
            },
            alterCourse () {
                const that = this
                that.teacherList.forEach(e => {
                    if (e.member_display_name === that.formData2.teacher) {
                        that.formData2.teacher_id = e.member_id
                    }
                })
                that.formData2.manage_student.forEach(e => {
                    const length = that.studentList.length
                    for (let i = 0; i < length; i++) {
                        if (that.studentList[i].member_display_name === e) {
                            that.formData2.manage_student_id.push(that.studentList[i].member_id)
                        }
                    }
                })
                this.$http.put('/course/manage_course/', this.formData2).then(res => {
                    if (res.result) {
                        this.getList()
                        this.$bkMessage({
                            message: res.message,
                            delay: 1000,
                            theme: 'success',
                            offsetY: 60,
                            ellipsisLine: 2 })
                    } else {
                        this.$bkMessage({
                            message: res.message,
                            delay: 1000,
                            theme: 'error',
                            offsetY: 60,
                            ellipsisLine: 2 })
                    }
                })
            },
            // 显示详情
            showDetail (e) {
                this.formData3 = e
                this.visible.introduction.isshow = true
            },
            // 页码改变
            pageChange () {
                const right = this.pagingConfigTwo.current * this.pagingConfigTwo.limit
                const left = right - this.pagingConfigTwo.limit
                this.List = this.course.slice(left, right)
            },
            // 页码的限制发生改变
            limitChange () {
                this.List = this.course.slice(0, this.pagingConfigTwo.limit)
            }
        }
    }
</script>

<style scoped>
    @import './my_course.css';
</style>
