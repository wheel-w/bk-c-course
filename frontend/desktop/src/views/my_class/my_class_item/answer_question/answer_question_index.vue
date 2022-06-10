<template>
    <div class="wrapper">
        <div class="content">
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
                <bk-table-column label="id" prop="id" width="50"></bk-table-column>
                <bk-table-column label="任务名称" prop="title">
                </bk-table-column>
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
                <bk-table-column label="学生是否可见" prop="students_visible" width="120">
                    <template slot-scope="props">
                        <div v-if="props.row.students_visible === true">
                            <p>是</p>
                        </div>
                        <div v-else>
                            <p>否</p>
                        </div>
                    </template>
                </bk-table-column>
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
                <bk-table-column label="创建人" prop="creator">
                    <template slot-scope="props">
                        <bk-popover placement="top" v-if="props.row.creator.length !== 0">
                            <span>{{props.row.creator.toString().slice(0,6) + (props.row.creator.toString().length > 6 ? '...' : '')}}</span>
                            <div slot="content">
                                <div class="bk-text pt10 pb5 pl10 pr10">{{props.row.creator}}</div>
                            </div>
                        </bk-popover>
                    </template>
                </bk-table-column>
                <bk-table-column label="更新人" prop="updater">
                    <template slot-scope="props">
                        <bk-popover placement="top" v-if="props.row.updater.length !== 0">
                            <span>{{props.row.updater.toString().slice(0,6) + (props.row.updater.toString().length > 6 ? '...' : '')}}</span>
                            <div slot="content">
                                <div class="bk-text pt10 pb5 pl10 pr10">{{props.row.updater}}</div>
                            </div>
                        </bk-popover>
                    </template>
                </bk-table-column>
                <bk-table-column label="我的得分" prop="total_score"></bk-table-column>
                <bk-table-column label="操作" align="center" header-align="center" width="200">
                    <template slot-scope="props">
                        <bk-button class="mr10" theme="primary" @click="startAnswer.primary.visible = true; startAnswer.primary.paperId = props.row.id;" text>开始答题</bk-button>
                        <bk-button class="mr10" theme="primary" @click="toAnalyze(props.row.id, true, true)" text>查看试卷解析</bk-button>
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
                taskList: [],
                project_task_id: ''
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
                this.$http.get(`/api/project-task/${this.project_id}/student/all/`).then(res => {
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
