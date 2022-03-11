<template>
    <div class="wrapper">
        <div class="wrapper1">
            <div class="wrapper-head" v-if="isManage">
                <bk-button :theme="'primary'" text class="mr10" @click="visible.addstudent.isshow = true">增加学生</bk-button>
                <bk-button :theme="'primary'" text class="mr10" @click="visible.addexcel.isshow = true">导入成员</bk-button>
                <bk-button :theme="'primary'" text class="mr10" @click="downtemplete">下载点名册模板</bk-button>
                <bk-button :theme="'primary'" text class="mr10" @click="visible.deleteall.isshow = true">批量删除</bk-button>
            </div>
            <div class="wrapper-body">
                <bk-table style="margin-top: 15px;"
                    size="small"
                    :data="data"
                    @selection-change="handleSelect"
                    @row-mouse-enter="handleRowMouseEnter"
                    @row-mouse-leave="handleRowMouseLeave"
                    @page-change="handlePageChange"
                    @page-limit-change="handlePageLimitChange">
                    <bk-table-column type="selection" width="60" align="center" header-align="center"></bk-table-column>
                    <bk-table-column type="index" label="序列" align="center" header-align="center" width="60"></bk-table-column>
                    <bk-table-column label="姓名" prop="name" align="center" header-align="center"></bk-table-column>
                    <bk-table-column label="学号" prop="class_number" align="center" header-align="center"></bk-table-column>
                    <bk-table-column label="专业班级" prop="professional_class" align="center" header-align="center"></bk-table-column>
                    <bk-table-column label="身份" prop="identify" align="center" header-align="center">
                        <template slot-scope="props">
                            <span v-if="props.row.identify === 'STUDENT'">学生</span>
                            <span v-if="props.row.identify === 'TEACHER'">老师</span>
                            <span v-if="props.row.identify === 'NOT_CERTIFIED'">未认证</span>
                        </template>
                    </bk-table-column>
                    <bk-table-column label="操作" width="150" align="center" header-align="center" v-if="isManage">
                        <template slot-scope="props">
                            <bk-button class="mr10" theme="primary" :disabled="props.row.identify === 'TEACHER'" text @click="beforRemove(props.row)">移除</bk-button>
                        </template>
                    </bk-table-column>
                </bk-table>
                <div style="padding-top: 10px;">
                    <bk-pagination
                        size="small"
                        :current.sync="page.current"
                        :limit.sync="page.limit"
                        :count="page.count"
                        :location="page.location"
                        :align="page.align"
                        :show-limit="page.showLimit"
                        :limit-list="page.limitList"
                        @change="pageChange"
                        @limit-change="limitChange">
                    </bk-pagination>
                </div>
            </div>
            <div id="dialog">
                <!-- 删除学生 -->
                <bk-dialog v-model="visible.deletestudent.isshow"
                    theme="primary"
                    :mask-close="false"
                    @confirm="removeStudent(student_id)"
                    :title="'删除学生'">
                    <div class="dialog-body">
                        你确定要删除{{studentInfo.name}}同学吗?
                    </div>
                </bk-dialog>
                <!-- 删除多个学生 -->
                <bk-dialog v-model="visible.deleteall.isshow"
                    width="530"
                    position="'top'"
                    :mask-close="false"
                    @confirm="removeStudent(student_id)">
                    <div class="dialog-body">
                        <p>确定要删除{{student_id.length}}项内容吗？</p>
                    </div>
                </bk-dialog>
                <!-- 增加学生 -->
                <bk-dialog v-model="visible.addstudent.isshow"
                    theme="primary"
                    width="530"
                    :mask-close="false"
                    @confirm="addStudent"
                    :title="'增加学生'">
                    <div style="text-align:center" v-if="addType === false">
                        <div class="dialog-body">
                            <bk-select style="width: 250px;margin-top: 10px;"
                                searchable
                                multiple
                                display-tag
                                v-model="addList">
                                <bk-option v-for="option in studentList"
                                    :key="option.member_id"
                                    :id="option.member_id"
                                    :name="option.member_display_name">
                                </bk-option>
                            </bk-select>
                        </div>
                        <bk-button :theme="'primary'" text @click="addType = true">学生未认证，点此添加</bk-button>
                    </div>
                    <div v-if="addType === true">
                        <bk-form :model="formData" ref="validateForm">
                            <bk-form-item
                                label="姓名"
                                :required="true"
                                :property="'name'"
                                :error-display-type="'normal'">
                                <bk-input v-model="formData.name" style="width: 250px;" placeholder="请输入姓名"></bk-input>
                            </bk-form-item>
                            <bk-form-item
                                label="学号"
                                :required="true"
                                :property="'class_number'"
                                :error-display-type="'normal'">
                                <bk-input v-model="formData.class_number" style="width: 250px;" placeholder="请输入学号"></bk-input>
                            </bk-form-item>
                        </bk-form>
                        <bk-button :theme="'primary'" text style="margin-left:90px;margin-top:20px" @click="addType = false">学生已认证，点此添加</bk-button>
                    </div>
                </bk-dialog>
                <!-- 导入学生 -->
                <bk-dialog v-model="visible.addexcel.isshow"
                    theme="primary"
                    :mask-close="false"
                    :show-footer="false"
                    :title="'导入学生名单'">
                    <div class="excel-dialog-body">
                        <div style="width:350px">
                            <bk-upload
                                :with-credentials="true"
                                :custom-request="addExcel"
                                :handle-res-code="handleRes"
                                :limit="1"
                                :tip="'只限上传.xls文件'"
                                :accept="'.xls'"
                                :delay-time="0"
                                @on-exceed="testExceed"
                            ></bk-upload>
                        </div>
                    </div>
                </bk-dialog>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'course_number',
        data () {
            return {
                addType: false,
                isManage: false, // 判断是否为管理员的表标识
                CourseData: [], // 课程的详细信息
                isHasTeacher: false, // 是否有老师
                studentList: [], // 所有认证过的学生
                addList: [], // 增加学生的id
                student_id: [], // 删除学生的id
                course_id: '', // 课程id
                formData: { // 学号+姓名增加
                    name: '',
                    class_number: ''
                },
                studentInfo: {},
                file: {}, // 文件
                data: [], // 学生列表
                page: {
                    current: 1,
                    limit: 10,
                    count: 30,
                    location: 'left',
                    align: 'right',
                    showLimit: true,
                    limitList: [10, 20, 30]
                },
                visible: {
                    addstudent: {
                        isshow: false
                    },
                    addexcel: {
                        isshow: false
                    },
                    deletestudent: {
                        isshow: false
                    },
                    deleteall: {
                        isshow: false
                    }
                }
            }
        },
        watch: {
            // 监听当前课程id的变化
            '$store.state.currentCourseId' (newValue) {
                this.course_id = this.$store.state.currentCourseId
                this.getList()
                // 判断当前用户是否为课程管理
                this.judgeManage()
            }
        },
        created () {
            this.course_id = this.$store.state.currentCourseId
            this.getList()
            this.$http.get('/course/find_courses/').then(res => { // 拿到所有课程信息
                if (res.result) {
                    this.CourseData = res.data
                }
            })
            this.userInfo = this.$store.state.user
            this.judgeManage()
        },
        methods: {
            getList () {
                const data = {}
                data.page_size = this.page.limit
                data.course_id = this.course_id
                data.page = this.page.current
                // 拿到当前页的课程成员信息
                this.$http.get('/course/search_course_student/', { params: data }).then(res => {
                    if (res.result) {
                        this.page.count = res.count
                        this.data = res.data
                    } else {
                        this.$bkMessage({
                            message: res.message,
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
            // 判断身份是否为管理员
            judgeManage () {
                if (this.$store.state.user.identity === 'TEACHER') {
                    this.isManage = true
                } else {
                    this.isManage = false
                    const that = this
                    this.CourseData.forEach(e => {
                        if (this.$store.state.currentCourseId === e.course_id) {
                            e.manage_student.forEach(re => {
                                const number = re.substring(0, re.indexOf('('))
                                if (number === this.userInfo.class_number) {
                                    that.isManage = true
                                }
                            })
                        }
                    })
                }
            },
            // 增加学生
            addStudent () {
                if (this.addType) {
                    if (this.formData.name === '' || this.formData.class_number === '') {
                        this.$bkMessage({
                            message: '请补全内容',
                            delay: 1000,
                            theme: 'error',
                            affsetY: 60,
                            ellipsisLine: 2
                        })
                    } else {
                        this.formData.course_id = this.course_id
                        this.$http.post('/course/add_course_member/', this.formData).then(res => {
                            if (res.result) {
                                this.$bkMessage({
                                    message: res.message,
                                    delay: 1000,
                                    theme: 'success',
                                    offsetY: 60,
                                    ellipsisLine: 2
                                })
                                this.getList()
                            } else {
                                this.$bkMessage({
                                    message: res.message,
                                    delay: 1000,
                                    theme: 'error',
                                    affsetY: 60,
                                    ellipsisLine: 2
                                })
                            }
                        })
                    }
                } else {
                    const data = {}
                    data.student_id = this.addList
                    data.course_id = this.course_id
                    this.$http.post('/course/add_course_student/', data).then(res => {
                        if (res.result) {
                            this.getList()
                            this.$bkMessage({
                                message: res.message,
                                delay: 1000,
                                theme: 'success',
                                offsetY: 60,
                                ellipsisLine: 2 })
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
                    this.addList = []
                }
            },
            // 导入学生
            addExcel (param) {
                // console.info(param)
                const data = new FormData()
                data.append('excel_file', param.fileList[0].origin)
                data.append('course_id', this.course_id)
                const config = {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
                this.$http.post('/course/import_student_excel/', data, config).then(res => {
                    if (res.result) {
                        this.getList()
                        this.$bkMessage({
                            message: '导入学生信息成功',
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
            handleRes (response) {
                if (response.result) {
                    return true
                }
                return false
            },
            // 下载点名册模板
            downtemplete () {
                const a = document.createElement('a')
                this.$http.get('/course/download_student_excel_template_url/').then(res => {
                    if (res.result) {
                        a.href = res.url
                        a.click()
                    } else {
                        this.$bkMessage({
                            message: '点名册模板下载失败请重新尝试',
                            delay: 1000,
                            theme: 'error',
                            offsetY: 60,
                            ellipsisLine: 2 })
                    }
                })
            },
            // 删除多个学生
            handleSelect (selection) {
                this.student_id = []
                selection.forEach(e => {
                    if (e.identify === 'TEACHER') {
                        this.isHasTeacher = true
                        console.info('有老师存在')
                    }
                    this.student_id.push(e.id)
                })
            },
            // 删除单个学生
            beforRemove (e) {
                this.student_id = []
                this.studentInfo = e
                this.student_id.push(e.id)
                this.visible.deletestudent.isshow = true
            },
            removeStudent (e) {
                this.$http.delete('/course/delete_student_course_contact/', { params: { course_id: this.course_id, student_id: JSON.stringify(e) } }).then(res => {
                    if (res.result) {
                        this.getList()
                        if (this.isHasTeacher) {
                            this.$bkMessage({
                                message: '老师无法删除',
                                delay: 1000,
                                theme: 'warning',
                                offsetY: 60,
                                ellipsisLine: 2 })
                        } else {
                            this.$bkMessage({
                                message: '删除成功',
                                delay: 1000,
                                theme: 'success',
                                offsetY: 60,
                                ellipsisLine: 2 })
                        }
                    } else {
                        this.$bkMessage({
                            message: '删除失败',
                            delay: 1000,
                            theme: 'error',
                            offsetY: 60,
                            ellipsisLine: 2 })
                    }
                })
            },
            // 分页
            pageChange () {
                this.getList()
            },
            // 页码的限制发生改变
            limitChange () {
                this.page.current = 1
                this.getList()
            }
        }
    }
</script>

<style scoped>
    @import './course_number.css';
</style>
