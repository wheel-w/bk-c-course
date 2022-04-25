<template>
    <div class="wrapper">
        <!--   <div class="wrapper-head" v-if="userIdentify === 'TEACHER'">-->
        <div class="wrapper-head">

            <bk-button theme="primary" class="mr10" :outline="true" @click="beforeAdd">创建项目</bk-button>
            <bk-button theme="primary" :outline="true" @click="removeallBefore">批量删除</bk-button>
        </div>
        <div class="wrapper-body">
            <bk-table style="margin-top: 10px"
                size="small"
                :data="List"
                :pagination="pagination"
                @selection-change="handleSelect"
                @row-mouse-enter="handleRowMouseEnter"
                @row-mouse-leave="handleRowMouseLeave"
                @page-change="handlePageChange"
                @page-limit-change="handlePageLimitChange">
                <!--v-if="userIdentify === 'TEACHER'"-->
                <bk-table-column type="selection" width="60" align="center" header-align="center"></bk-table-column>
                <bk-table-column label="项目id" prop="id" align="center" header-align="center"></bk-table-column>
                <bk-table-column label="项目名称" prop="name" align="center" header-align="center"></bk-table-column>
                <bk-table-column label="项目简介" prop="introduction" align="center" header-align="center"></bk-table-column>
                <bk-table-column label="项目性质" prop="property" align="center" header-align="center"></bk-table-column>
                <bk-table-column label="项目归属" prop="category" align="center" header-align="center"></bk-table-column>
                <bk-table-column label="组织名称" prop="organization" align="center" header-align="center"></bk-table-column>
                <bk-table-column label="创建人" prop="creator" align="center" header-align="center"></bk-table-column>
                <bk-table-column label="创建时间" prop="create_time" align="center" header-align="center"></bk-table-column>
                <bk-table-column label="更新时间" prop="update_time" align="center" header-align="center"></bk-table-column>
                <!-- v-if="userIdentify === 'TEACHER'"-->
                <bk-table-column label="操作" width="150" align="center" header-align="center">
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
                width="1200"
                position="top"
                :mask-close="false"
                :header-position="visible.addcourse.headerPosition"
                :confirm-fn="Check"
                @confirm="addCourse"
                title="创建项目">
                <bk-form :model="formData" :rules="rules" ref="validateForm">
                    <bk-form-item
                        :required="true"
                        :property="'name'"
                        :error-display-type="'normal'">
                        <bk-input v-model="formData.name" style="width: 350px; margin-left: 250px" placeholder="请输入项目名称"></bk-input>
                    </bk-form-item>
                    <bk-form-item>
                        <bk-input type="textarea" style="width: 350px; margin-left: 250px" v-model="formData.introduction" placeholder="在这里输入项目简介"></bk-input>
                    </bk-form-item>
                    <bk-form-item :required="true" class="add-course-form-item">
                        <h3>项目性质</h3>
                        <img src="../../../../images/icon_properties.png" alt="">
                        <bk-input type="textarea" style="width: 180px;" v-model="formData.property" placeholder="在这里输入项目性质"></bk-input>
                    </bk-form-item>
                    <bk-form-item :required="true" class="add-course-form-item">
                        <h3>项目归属</h3>
                        <img src="../../../../images/icon_bg.png" alt="">
                        <bk-input type="textarea" style="width: 180px;" v-model="formData.category" placeholder="在这里输入项目归属"></bk-input>
                    </bk-form-item>
                    <bk-form-item :required="true" class="add-course-form-item">
                        <h3>组织名称</h3>
                        <img src="../../../../images/icon_bg.png" alt="">
                        <bk-input type="textarea" style="width: 180px;" v-model="formData.organization" placeholder="在这里输入组织名称"></bk-input>
                    </bk-form-item>
                </bk-form>
                <div slot="footer">
                    <bk-button theme="primary" class="mr10" @click="addCourse">创建</bk-button>
                    <bk-button theme="primary" class="mr10" @click="visible.addcourse.isshow = false">取消</bk-button>
                </div>
            </bk-dialog>
            <!-- 删除课程 -->
            <bk-dialog v-model="visible.deletcourse.isshow"
                width="530"
                position="'top'"
                :mask-close="false"
                :header-position="visible.addcourse.headerPosition"
                :title="'删除除课程'"
                @confirm="removeCourse(id)">
                <div class="dialog-body">
                    <p>确定要删除{{formData3.name}}这门课程吗</p>
                </div>
            </bk-dialog>
            <!-- 批量删除 -->
            <bk-dialog v-model="visible.deleteall.isshow"
                width="530"
                position="'top'"
                :mask-close="false"
                :header-position="visible.deleteall.headerPosition"
                @confirm="removeMultiCourse(id)">
                <div class="dialog-body">
                    <p>确定要删除{{id.length}}项内容吗？</p>
                </div>
            </bk-dialog>
            <!-- 修改课程 -->
            <bk-dialog v-model="visible.altercourse.isshow"
                width="1200"
                position="'top'"
                :mask-close="false"
                style="margin-top: 20px"
                :header-position="visible.addcourse.headerPosition"
                title="编辑项目信息"
                @confirm="alterCourse">
                <bk-form :model="formData2" :rules="rules" ref="validateForm">
                    <bk-form-item
                        :required="true"
                        :property="'course_name'"
                        :error-display-type="'normal'">
                        <bk-input v-model="formData2.name" style="width: 350px; margin-left: 250px" placeholder="请输入课程名称"></bk-input>
                    </bk-form-item>
                    <bk-form-item>
                        <bk-input type="textarea" style="width: 350px; margin-left: 250px" v-model="formData2.introduction" placeholder="在这里输入项目简介"></bk-input>
                    </bk-form-item>
                    <bk-form-item :required="true" class="add-course-form-item">
                        <img src="../../../../images/icon_properties.png">
                        <h3>项目性质</h3>
                        <bk-input type="textarea" style="width: 180px;" v-model="formData2.property" placeholder="在这里输入项目性质"></bk-input>
                    </bk-form-item>
                    <bk-form-item :required="true" class="add-course-form-item">
                        <img src="../../../../images/icon_bg.png">
                        <h3>项目归属</h3>
                        <bk-input type="textarea" style="width: 180px;" v-model="formData2.category" placeholder="在这里输入项目性质"></bk-input>
                    </bk-form-item>
                    <bk-form-item :required="true" class="add-course-form-item">
                        <img src="../../../../images/icon_bg.png">
                        <h3>组织名称</h3>
                        <bk-input type="textarea" style="width: 180px;" v-model="formData2.organization" placeholder="在这里输入组织名称"></bk-input>
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
                // course: [],
                teacherList: [],
                studentList: [],
                course_id: [],
                List: [],
                formData: {
                    name: '',
                    introduction: '',
                    property: '',
                    category: '',
                    organization: ''

                },
                formData2: {
                    id: '',
                    name: '',
                    introduction: '',
                    property: '',
                    category: '',
                    organization: ''
                },
                formData3: '',
                visible: { // 这是对话框的显示控制
                    addcourse: {
                        isshow: false,
                        headerPosition: 'left'
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
                },
                id: []
            }
        },
        created () {
            this.getList()
            this.userIdentify = this.$store.state.user.identity
            this.timeReverse()
        },
        mounted () {
            this.$nextTick(() => {
                this.timeReverse()
            })
            const that = this
            setTimeout(function () {
                that.timeReverse()
            }, 2000)
        },
        methods: {
            getList () {
                // 拿到课程信息
                this.$http.get('/api/project/', { params: { page: this.pagingConfigTwo.current, page_size: this.pagingConfigTwo.limit } }).then(res => {
                    console.log('获取项目列表', res)
                    if (res.result) {
                        console.log('res', res)
                        this.pagingConfigTwo.count = res.data.count
                        this.List = res.data.results
                        this.timeReverse()
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
            // 创建项目
            addCourse () {
                if (this.formData.name === '' || this.formData.introduction === '' || this.formData.property === ''
                    || this.formData.category === '' || this.formData.organization === '') {
                    this.$bkMessage({
                        message: '请补全内容',
                        delay: 1000,
                        theme: 'error',
                        offsetY: 60,
                        ellipsisLine: 2 })
                    this.visible.addcourse.isshow = true
                } else {
                    this.$http.post('/api/project/', this.formData).then(res => {
                        console.log('createProject', res)
                        if (res.result) {
                            this.$bkMessage({
                                message: '创建成功',
                                delay: 1000,
                                theme: 'success',
                                offsetY: 60,
                                ellipsisLine: 2 })
                            this.getList()
                            this.visible.addcourse.isshow = false
                            this.formData.name = ''
                            this.formData.introduction = ''
                            this.formData.property = ''
                            this.formData.category = ''
                            this.formData.organization = ''
                            this.$store.commit('updateCourseId', 0)

                            this.List = this.course.slice(0, this.pagingConfigTwo.limit)
                        } else {
                            this.$bkMessage({
                                message: '创建失败，请重试',
                                delay: 1000,
                                theme: 'error',
                                offsetY: 60,
                                ellipsisLine: 2 })
                            this.visible.addcourse.isshow = false
                        }
                    })
                }
            },
            // 删除多项
            handleSelect (selection) {
                this.id = []
                selection.forEach(e => {
                    this.id.push(e.id)
                })
            },
            removeallBefore () {
                if (this.id.length !== 0) {
                    this.visible.deleteall.isshow = true
                }
            },
            removeMultiCourse (e) {
                this.$http.delete('/api/project/bulk_delete/', { data: { project_id_list: this.id } }).then(res => {
                    if (res.result) {
                        this.$bkMessage({
                            message: '删除成功',
                            delay: 1000,
                            theme: 'success',
                            offsetY: 60,
                            ellipsisLine: 2 })
                        this.getList()
                    } else {
                        this.$bkMessage({
                            message: '删除失败',
                            delay: 1000,
                            theme: 'error',
                            offsetY: 60,
                            ellipsisLine: 2 })
                        this.getList()
                    }
                })
                this.getList()
            },
            // 删除单个课程
            removeBefor (e) {
                this.id = []
                this.formData3 = e
                this.id.push(e.id)
                this.visible.deletcourse.isshow = true
                console.log('id', this.id)
            },
            // 删除项目
            removeCourse (e) {
                this.$http.delete('/api/project/' + this.id[0] + '/').then(res => {
                    console.log('删除项目res', res)
                    if (res.result) {
                        this.$bkMessage({
                            message: '删除成功',
                            delay: 1000,
                            theme: 'success',
                            offsetY: 60,
                            ellipsisLine: 2 })
                        this.getList()
                    } else {
                        this.$bkMessage({
                            message: '删除失败',
                            delay: 1000,
                            theme: 'error',
                            offsetY: 60,
                            ellipsisLine: 2 })
                        this.getList()
                    }
                })
                this.formData3 = ''
            },
            // 修改课程
            alterBefore (e) {
                this.formData2.id = e.id
                this.formData2.name = e.name
                this.formData2.introduction = e.introduction
                this.formData2.property = e.property
                this.formData2.category = e.category
                this.formData2.organization = e.organization
                this.visible.altercourse.isshow = true
            },
            alterCourse () {
                this.$http.put('/api/project/' + this.formData2.id + '/', this.formData2).then(res => {
                    if (res.result) {
                        this.getList()
                        this.$bkMessage({
                            message: '修改成功！',
                            delay: 1000,
                            theme: 'success',
                            offsetY: 60,
                            ellipsisLine: 2 })
                    } else {
                        this.$bkMessage({
                            message: '修改失败',
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
                this.getList()
            },
            // 页码的限制发生改变
            limitChange () {
                this.getList()
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
            timeFormatSeconds (time) {
                const d = time ? new Date(time) : new Date()
                const year = d.getFullYear()
                let month = d.getMonth() + 1
                let day = d.getDate()
                let hours = d.getHours()
                let min = d.getMinutes()
                let seconds = d.getSeconds()

                if (month < 10) month = '0' + month
                if (day < 10) day = '0' + day
                if (hours < 0) hours = '0' + hours
                if (min < 10) min = '0' + min
                if (seconds < 10) seconds = '0' + seconds

                return (year + '-' + month + '-' + day + ' ' + hours + ':' + min + ':' + seconds)
            },
            timeReverse () {
                for (const item in this.List) {
                    this.List[item]['create_time'] = this.msToDate((this.List[item]['create_time'])).hasTime
                    this.List[item]['update_time'] = this.msToDate((this.List[item]['update_time'])).hasTime
                }
            }
        }
    }
</script>

<style lang="postcss">
    @import './my_course.css';
    .bk-button.bk-primary.is-outline {
        color: #fff;
        border-color: #88a2ef;
        background-color: #fff;
    }
    .bk-button.bk-primary {
        background: #88a2ef !important;
        border-color: #88a2ef;
        color: #fff;
    }
    .page-button{
        background-color: #88a2ef !important;
        color: #f6f6f6;
        border-radius: 5px;
    }
    .bk-page .page-item.cur-page .page-button{
        color: #f6f6f6 !important;
    }
    .bk-dialog-content{
        background-image: url('../../../../images/add_dialog_bg.png');
    }
    .bk-dialog-footer{
        background-color: #cbd2e6 !important;
    }
    .add-course-form-item{
        background-color: #ffffff;
        width: 360px;
        height: 120px;
        border: 1px solid #d4d4d4;
        border-radius: 10px;
        box-shadow: 10px 10px 5px #888888;
        float: left;
        margin: 5px 10px ;
    }
    .add-course-form-item img{
        position: absolute;
        top: 35px;
        left: -130px;
    }
    .add-course-form-item h3{
        color: #717fa2;
        position: absolute;
        top: 30px;
        left: -70px;
    }
    .add-course-form-item .bk-select{
        position: absolute;
        top: 65px;
        left: 20px;
    }
    .add-course-form-item .bk-textarea-wrapper{
        position: absolute;
        top: 10px;
        left: 15px;
    }
    .bk-form-input{
        height: 40px !important;
    }
</style>
