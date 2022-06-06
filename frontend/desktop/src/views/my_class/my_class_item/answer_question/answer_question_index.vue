<template>
    <div class="wrapper">
        <div class="content">
            <bk-button theme="primary"
                :outline="true"
                style="margin-bottom: 20px; background: #88a2ef;"
                @click="removeMultiBefor"
                :disabled="task_id_list.length === 0">批量删除</bk-button>
            <bk-table :data="taskList"
                :size="'small'"
                height="450"
                :outer-border="false"
                :header-border="false"
                :pagination="pagination"
                :virtual-render="true"
                @selection-change="handleSelect"
                @page-change="handlePageChange"
                @page-limit-change="handlePageLimitChange">
                <bk-table-column type="selection" align="center" header-align="center"></bk-table-column>
                <bk-table-column label="id" prop="id" width="50"></bk-table-column>
                <bk-table-column label="任务名称" prop="title"></bk-table-column>
                <bk-table-column label="任务描述" prop="describe">
                    <template slot-scope="props">
                        <bk-popover placement="top" v-if="props.row.describe.length !== 0">
                            <span>{{props.row.describe.toString().slice(0,5) + (props.row.describe.toString().length > 5 ? '...' : '')}}</span>
                            <div slot="content">
                                <div class="bk-text pt10 pb5 pl10 pr10">{{props.row.describe}}</div>
                            </div>
                        </bk-popover>
                    </template>
                </bk-table-column>
                <bk-table-column label="类型"
                    prop="types"
                    width="90"
                    :filters="typesFilters"
                    :filter-multiple="false"
                    :filter-method="filterMethod">
                    <template slot-scope="props">
                        <bk-tag v-if="props.row.types === '日常任务'" type="stroke" style="margin: 0; padding: 0 2px;">日常任务</bk-tag>
                        <bk-tag v-else theme="info" type="stroke" style="margin: 0; padding: 0 2px;">考核任务</bk-tag>
                    </template>
                </bk-table-column>
                <bk-table-column label="状态"
                    prop="status"
                    :filters="statusFilters"
                    :filter-multiple="false"
                    :filter-method="filterMethod">
                    <template slot-scope="props">
                        <bk-tag v-if="props.row.status === '草稿'" theme="warning" type="stroke" style="margin: 0; padding: 0 2px;">草稿</bk-tag>
                        <bk-tag v-else theme="success" type="stroke" style="margin: 0; padding: 0 2px;">已发布</bk-tag>
                    </template>
                </bk-table-column>
                <bk-table-column label="学生是否可见" prop="students_visible">
                    <template slot-scope="props">
                        <div v-if="props.row.students_visible === true">
                            <p>是</p>
                        </div>
                        <div v-else>
                            <p>否</p>
                        </div>
                    </template>
                </bk-table-column>
                <bk-table-column label="需要完成人数" prop="student_total_count"></bk-table-column>
                <bk-table-column label="提交人数" prop="submitted_count"></bk-table-column>
                <bk-table-column label="批阅数量" prop="marked_count"></bk-table-column>
                <bk-table-column label="开始时间" prop="start_time" width="100">
                    <template slot-scope="props">
                        <bk-popover placement="top" v-if="props.row.start_time.length !== 0">
                            <span>{{props.row.start_time.toString().slice(0,10) + (props.row.start_time.toString().length > 10 ? '' : '')}}</span>
                            <div slot="content">
                                <div class="bk-text pt10 pb5 pl10 pr10">{{props.row.start_time}}</div>
                            </div>
                        </bk-popover>
                    </template>
                </bk-table-column>
                <bk-table-column label="截止时间" prop="end_time" width="100">
                    <template slot-scope="props">
                        <bk-popover placement="top" v-if="props.row.end_time.length !== 0">
                            <span>{{props.row.end_time.toString().slice(0,10) + (props.row.end_time.toString().length > 10 ? '' : '')}}</span>
                            <div slot="content">
                                <div class="bk-text pt10 pb5 pl10 pr10">{{props.row.end_time}}</div>
                            </div>
                        </bk-popover>
                    </template>
                </bk-table-column>
                <bk-table-column label="操作" align="center" width="240" header-align="center">
                    <template slot-scope="props">
                        <bk-button class="mr10" theme="primary" @click="startAnswer.primary.visible = true; startAnswer.primary.paperId = props.row.id;" text>开始答题</bk-button>
                        <bk-button class="mr10" theme="primary" text @click="removeBefor(props.row)">删除</bk-button>
                        <bk-button class="mr10" v-if="props.row.status === '草稿'" theme="primary" text @click="releaseBefor(props.row)">定时发布</bk-button>
                        <bk-button class="mr10" v-if="props.row.status === '草稿'" theme="primary" text @click="releaseNowBefor(props.row)">立即发布</bk-button>
                        <bk-button class="mr10" v-else-if="props.row.status === '已发布'" theme="primary" text @click="cancleBefor(props.row)">取消发布</bk-button>

                    </template>
                </bk-table-column>
            </bk-table>
            <div id="dialog">
                <bk-dialog v-model="startAnswer.primary.visible" @confirm="toAnswer(startAnswer.primary.paperId, false)"
                    theme="primary"
                    :mask-close="false"
                    :header-position="startAnswer.primary.head"
                    title="开始答题">
                    是否确认开始答题？
                </bk-dialog>
                <!--删除任务-->
                <bk-dialog v-model="deleteTaskDialog.primary.visible"
                    theme="primary"
                    :mask-close="true"
                    @confirm="removeTask(id)"
                    :header-position="deleteTaskDialog.primary.head"
                    title="删除任务">
                    是否要删除该任务？
                </bk-dialog>
                <!-- 批量删除 -->
                <bk-dialog v-model="deleteAllTaskDialog.primary.visible"
                    width="530"
                    position="'top'"
                    :mask-close="false"
                    :header-position="deleteAllTaskDialog.primary.head"
                    @confirm="removeMultiTask(id)">
                    <div class="dialog-body">
                        <h3>确定要删除{{task_id_list.length}}项内容吗？</h3>
                    </div>
                </bk-dialog>
                <!--定时发布任务-->
                <bk-dialog v-model="releaseTaskDialog.primary.visible"
                    theme="primary"
                    :mask-close="true"
                    @confirm="releaseTask(id)"
                    :header-position="releaseTaskDialog.primary.visible"
                    title="发布任务">
                    <!--请选择计划发布时间：-->
                    <bk-date-picker v-model="scheduledPublishTime" :placeholder="'请选择计划发布日期时间'" :type="'datetime'"></bk-date-picker>
                </bk-dialog>
                <!--立即发布任务-->
                <bk-dialog v-model="releaseNowTaskDialog.primary.visible"
                    theme="primary"
                    :mask-close="true"
                    @confirm="releaseNowTask(id)"
                    :header-position="releaseNowTaskDialog.primary.visible"
                    title="发布任务">
                    是否要立即发布当前任务？
                </bk-dialog>
                <!--取消发布任务-->
                <bk-dialog v-model="cancleReleaseTaskDialog.primary.visible"
                    theme="primary"
                    :mask-close="true"
                    @confirm="cancleReleaseTask(id)"
                    :header-position="cancleReleaseTaskDialog.primary.visible"
                    title="取消发布任务">
                    确认要取消发布该任务嘛？
                </bk-dialog>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'answer_question_index',
        data () {
            return {
                // 分页器配置项
                pagination: {
                    current: 1,
                    count: 0,
                    limit: 10
                },
                // 确认是否答题控制
                startAnswer: {
                    primary: {
                        visible: false,
                        headerPosition: 'left',
                        paperId: 0
                    }
                },
                // 删除任务
                deleteTaskDialog: {
                    primary: {
                        visible: false,
                        head: 'left'
                    }
                },
                deleteAllTaskDialog: {
                    primary: {
                        visible: false,
                        head: 'left'
                    }
                },
                releaseTaskDialog: {
                    primary: {
                        visible: false,
                        head: 'left'
                    }
                },
                releaseNowTaskDialog: {
                    primary: {
                        visible: false,
                        head: 'left'
                    }
                },
                cancleReleaseTaskDialog: {
                    primary: {
                        visible: false,
                        head: 'left'
                    }
                },
                taskList: [],
                typesFilters: [
                    {
                        value: '日常任务',
                        text: '日常任务'
                    },
                    {
                        value: '考核任务',
                        text: '考核任务'
                    }
                ],
                statusFilters: [
                    {
                        value: '草稿',
                        text: '草稿'
                    },
                    {
                        value: '已发布',
                        text: '已发布'
                    }
                ],
                scheduledPublishTime: new Date(),
                publishTaskForm: [],
                project_task_id: '',
                task_id_list: []
            }
        },
        watch: {
            // 监听当前课程id的变化
            '$store.state.currentCourseId' () {
                this.project_id = this.$store.state.currentCourseId
                // 发送网络请求更新课程信息
                this.getTaskList()
            }
        },
        mounted () {
            setTimeout(() => {
                this.getTaskList()
            }, 50)
        },
        created () {
            this.getParams()
            // this.project_id = this.$store.state.currentCourseId
        },
        methods: {
            // 接收参数
            getParams () {
                this.project_id = this.$route.params.projectId
            },
            // 过滤状态、类型、可见范围
            filterMethod (value, row, column) {
                const property = column.property
                return row[property] === value
            },
            // 删除任务
            removeBefor (e) {
                this.project_task_id = ''
                this.project_task_id = e.id
                this.deleteTaskDialog.primary.visible = true
            },
            // 确认删除任务
            removeTask (e) {
                this.$http.delete(`/api/project-task/${this.project_task_id}/`).then(res => {
                    if (res.result) {
                        this.$bkMessage({
                            message: '删除成功',
                            delay: 1000,
                            theme: 'success',
                            offsetY: 60,
                            ellipsisLine: 2 })
                        this.getTaskList()
                    } else {
                        this.$bkMessage({
                            message: '删除失败',
                            delay: 1000,
                            theme: 'error',
                            offsetY: 60,
                            ellipsisLine: 2 })
                        this.getTaskList()
                    }
                })
                this.getTaskList()
                this.project_task_id = ''
            },
            // 删除多项
            handleSelect (selection) {
                this.task_id_list = []
                selection.forEach(e => {
                    this.task_id_list.push(e.id)
                })
            },
            removeMultiBefor () {
                if (this.task_id_list.length !== 0) {
                    this.deleteAllTaskDialog.primary.visible = true
                }
            },
            // 确认删除多项
            removeMultiTask (e) {
                this.$http.delete('/api/project-task/', { data: { 'task_id_list': this.task_id_list } }).then(res => {
                    if (res.result) {
                        this.$bkMessage({
                            message: '批量删除成功',
                            delay: 1000,
                            theme: 'success',
                            offsetY: 60,
                            ellipsisLine: 2 })
                        this.getTaskList()
                    } else {
                        this.$bkMessage({
                            message: '批量删除失败',
                            delay: 1000,
                            theme: 'error',
                            offsetY: 60,
                            ellipsisLine: 2 })
                        this.getTaskList()
                    }
                })
                this.getTaskList()
                this.project_task_id = []
            },
            // 定时发布任务
            releaseBefor (e) {
                this.project_task_id = e.id
                this.releaseTaskDialog.primary.visible = true
            },
            // 确认定时发布任务
            releaseTask (e) {
                this.scheduledPublishTime = this.msToDate((this.scheduledPublishTime)).hasTime
                this.scheduledPublishTime = this.scheduledPublishTime.replace(/ /g, 'T')
                console.log('this.scheduled_publish_time', this.scheduledPublishTime)
                this.$http.patch(`/api/project-task/${this.project_task_id}/`, { 'scheduled_publish_time': this.scheduledPublishTime }).then(res => {
                    console.log('定时发布res：', res)
                    if (res.result) {
                        this.$bkMessage({
                            message: '发布成功',
                            delay: 1000,
                            theme: 'success',
                            offsetY: 60,
                            ellipsisLine: 2 })
                        this.getTaskList()
                    } else {
                        this.$bkMessage({
                            message: '发布失败',
                            delay: 1000,
                            theme: 'error',
                            offsetY: 60,
                            ellipsisLine: 2 })
                        this.getTaskList()
                    }
                })
                this.getTaskList()
                this.id = []
            },
            // 立即发布任务
            releaseNowBefor (e) {
                this.project_task_id = e.id
                this.releaseNowTaskDialog.primary.visible = true
            },
            // 确认立即发布任务
            releaseNowTask (e) {
                this.$http.patch(`/api/project-task/${this.project_task_id}/`, { 'status': 'RELEASE' }).then(res => {
                    if (res.result) {
                        this.$bkMessage({
                            message: '发布成功',
                            delay: 1000,
                            theme: 'success',
                            offsetY: 60,
                            ellipsisLine: 2 })
                        this.getTaskList()
                    } else {
                        this.$bkMessage({
                            message: '发布失败',
                            delay: 1000,
                            theme: 'error',
                            offsetY: 60,
                            ellipsisLine: 2 })
                        this.getTaskList()
                    }
                })
                this.getTaskList()
                this.id = []
            },
            // 取消发布任务
            cancleBefor (e) {
                this.publishTaskForm = []
                this.publishTaskForm = e
                this.project_task_id = e.id
                this.cancleReleaseTaskDialog.primary.visible = true
            },
            // 确认取消发布任务
            cancleReleaseTask (e) {
                // this.publishTaskForm.status = 'DRAFT'
                this.$http.patch(`/api/project-task/${this.project_task_id}/`, { 'status': 'DRAFT' }).then(res => {
                    console.log('res', res)
                    if (res.result) {
                        this.$bkMessage({
                            message: '取消发布成功',
                            delay: 1000,
                            theme: 'success',
                            offsetY: 60,
                            ellipsisLine: 2 })
                        this.getTaskList()
                    } else {
                        this.$bkMessage({
                            message: '取消发布失败',
                            delay: 1000,
                            theme: 'error',
                            offsetY: 60,
                            ellipsisLine: 2 })
                        this.getTaskList()
                    }
                })
                this.getTaskList()
                this.project_task_id = ''
            },
            // 跳转答题页面
            toAnswer (id, isAccomplish) {
                this.startAnswer.primary.visible = false
                this.$router.push({
                    name: 'answer_question_detail',
                    query: {
                        id,
                        isAccomplish,
                        'project_id': this.project_id
                    }
                })
            },
            // 跳转试卷分析页面
            toAnalyze (id, isAccomplish, isMarked) {
                this.$router.push({
                    name: 'answer_question_detail',
                    query: {
                        id,
                        isAccomplish,
                        isMarked
                    }
                })
            },
            // 监听pagination的限制个数变化
            handlePageLimitChange () {
                this.pagination.limit = arguments[0]
                this.pagination.current = 1
                this.updateCurrentExerciseList()
            },
            // 监听pagination的当前页码发生变化
            handlePageChange (page) {
                this.pagination.current = page
                this.updateCurrentExerciseList()
            },
            getTaskList () {
                this.taskList = []
                this.$http.get(`/api/project-task/${this.project_id}/teacher/all/`).then(res => {
                    console.log('获取任务列表后端返回的数据', res)
                    this.taskList = res.data
                    this.timeReverse()
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
            timeReverse () {
                for (const item in this.taskList) {
                    this.taskList[item]['time_created'] = this.msToDate((this.taskList[item]['time_created'])).hasTime
                    this.taskList[item]['time_updated'] = this.msToDate((this.taskList[item]['time_updated'])).hasTime
                    this.taskList[item]['start_time'] = this.msToDate((this.taskList[item]['start_time'])).hasTime
                    this.taskList[item]['end_time'] = this.msToDate((this.taskList[item]['end_time'])).hasTime
                }
            }
        }
    }
</script>

<style lang="postcss">
.content {
    margin-top: 20px;
    }
    .page-button{
        background-color: #88a2ef !important;
        color: #f6f6f6;
        border-radius: 5px;
    }
    .bk-page .page-item.cur-page .page-button{
        color: #f6f6f6 !important;
    }
    .custom-tag {
        color: #531dab;
        background: #f9f0ff;
    }
</style>
