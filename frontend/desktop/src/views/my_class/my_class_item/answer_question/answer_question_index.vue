<template>
    <div class="wrapper">
        <div class="content">
            <bk-table :data="currentExerciseList"
                :size="'media'"
                max-height="560"
                :pagination="pagination"
                @filter-change="changeList"
                @page-change="handlePageChange"
                @page-limit-change="handlePageLimitChange">
                <bk-table-column type="index" label="序号" width="100"></bk-table-column>
                <bk-table-column label="章节名称" prop="chapter_name" width="150" :filters="chapterStatusFilters" :filter-multiple="false"></bk-table-column>
                <bk-table-column label="习题名称" width="150">
                    <template slot-scope="props">
                        <div>
                            <bk-button v-if="props.row.student_status === 'NOTSTART'" theme="primary" text disabled>{{ props.row.paper_name }}</bk-button>
                            <bk-button v-else-if="props.row.student_status === 'REALSUBMITTED'" theme="primary" text @click="toAnswer(props.row.id, false)">{{ props.row.paper_name }}</bk-button>
                            <bk-button v-else-if="props.row.student_status === 'REALMARKED'" theme="primary" text @click="toAnalyze(props.row.id, true)">{{ props.row.paper_name }}</bk-button>
                            <bk-button v-else-if="props.row.student_status === 'UNDERWAY'" theme="primary" text @click="startAnswer.primary.visible = true; startAnswer.primary.paperId = props.row.id;">{{ props.row.paper_name }}</bk-button>
                            <bk-button v-else-if="props.row.student_status === 'FINISHED'" theme="primary" text @click="toAnswer(props.row.id, false)">{{ props.row.paper_name }}</bk-button>
                        </div>
                    </template>
                </bk-table-column>
                <bk-table-column label="开始时间" prop="start_time" width="200"></bk-table-column>
                <bk-table-column label="截止时间" prop="end_time" width="200"></bk-table-column>
                <bk-table-column label="我的分数" prop="score" width="100">
                    <template slot-scope="props">
                        {{ props.row.student_status === 'REALMARKED' ? props.row.score : '———' }}
                    </template>
                </bk-table-column>
                <bk-table-column label="习题状态" width="150" prop="student_status" :filters="statusFilters" :filter-multiple="true">
                    <template slot-scope="props">
                        <bk-tag v-if="props.row.student_status === 'NOTSTART'" theme="filled" radius="10px" type="filled">未开始</bk-tag>
                        <bk-tag v-else-if="props.row.student_status === 'REALSUBMITTED'" theme="warning" radius="10px" type="filled">已提交</bk-tag>
                        <bk-tag v-else-if="props.row.student_status === 'REALMARKED'" theme="info" radius="10px" type="filled">已批改</bk-tag>
                        <bk-tag v-else-if="props.row.student_status === 'UNDERWAY'" theme="success" radius="10px" type="filled">进行中</bk-tag>
                        <bk-tag v-else-if="props.row.student_status === 'FINISHED'" theme="danger" radius="10px" type="filled">已结束</bk-tag>
                    </template>
                </bk-table-column>
                <bk-table-column label="操作">
                    <template slot-scope="props">
                        <div>
                            <bk-button v-if="props.row.student_status === 'NOTSTART'" theme="primary" text disabled>暂未开始</bk-button>
                            <bk-button v-else-if="props.row.student_status === 'REALSUBMITTED'" theme="primary" text @click="toAnswer(props.row.id, false)">查看作答情况</bk-button>
                            <bk-button v-else-if="props.row.student_status === 'REALMARKED'" theme="primary" text @click="toAnalyze(props.row.id, true)">查看解析</bk-button>
                            <bk-button v-else-if="props.row.student_status === 'UNDERWAY'" theme="primary" text @click="startAnswer.primary.visible = true; startAnswer.primary.paperId = props.row.id;">开始答题</bk-button>
                            <bk-button v-else-if="props.row.student_status === 'FINISHED'" theme="primary" text @click="toAnswer(props.row.id, false)">查看作答情况</bk-button>
                        </div>
                    </template>
                </bk-table-column>
            </bk-table>
            <bk-dialog v-model="startAnswer.primary.visible" @confirm="toAnswer(startAnswer.primary.paperId, false)"
                theme="primary"
                :mask-close="false"
                :header-position="startAnswer.primary.headerPosition"
                title="开始答题">
                是否确认开始答题？
            </bk-dialog>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'answer_question_index',
        data () {
            return {
                // 试卷状态过滤器
                statusFilters: [
                    {
                        text: '进行中',
                        value: 'UNDERWAY'
                    },
                    {
                        text: '已提交',
                        value: 'REALSUBMITTED'
                    },
                    {
                        text: '已批改',
                        value: 'REALMARKED'
                    },
                    {
                        text: '已结束',
                        value: 'FINISHED'
                    },
                    {
                        text: '未开始',
                        value: 'NOTSTART'
                    }
                ],
                // 习题章节过滤器
                chapterStatusFilters: [],
                // 总习题列表
                exerciseList: [],
                // 当前页习题列表
                currentExerciseList: [],
                // 中间习题列表
                middleExerciseList: [],
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
                }
            }
        },
        watch: {
            // 监听当前课程id的变化
            '$store.state.currentCourseId' () {
                // 发送网络请求更新课程信息
                this.getExerciseList()
            }
        },
        mounted () {
            setTimeout(() => {
                this.getExerciseList()
            }, 50)
        },
        methods: {
            // 过滤状态和章节
            changeList (filters) {
                this.middleExerciseList = []
                for (const item in filters) {
                    if (filters[item].length !== 0) {
                        for (const i of filters[item]) {
                            let list = []
                            if (typeof i === 'string') {
                                list = this.exerciseList.filter(exerciseItem => {
                                    return exerciseItem.student_status === i
                                })
                            }
                            if (typeof i === 'number') {
                                list = this.exerciseList.filter(exerciseItem => {
                                    return exerciseItem.chapter_id === i
                                })
                            }

                            this.middleExerciseList.push(...list)
                        }
                    } else {
                        this.middleExerciseList = this.exerciseList
                    }
                }
                this.pagination.current = 1
                this.pagination.count = this.middleExerciseList.length
                this.updateCurrentExerciseList()
            },
            // 跳转答题页面
            toAnswer (id, isAccomplish) {
                this.startAnswer.primary.visible = false
                this.$router.push({
                    name: 'answer_question_detail',
                    query: {
                        id,
                        isAccomplish
                    }
                })
            },
            // 跳转试卷分析页面
            toAnalyze (id, isAccomplish) {
                this.$router.push({
                    name: 'answer_question_detail',
                    query: {
                        id,
                        isAccomplish
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
            // 更新当前数组列表
            updateCurrentExerciseList () {
                this.currentExerciseList = []

                let interceptLength = this.pagination.limit * this.pagination.current
                if (interceptLength > this.pagination.count) {
                    interceptLength = this.pagination.count
                }

                for (let i = (this.pagination.current - 1) * this.pagination.limit; i < interceptLength; i++) {
                    this.middleExerciseList[i].start_time = this.dayjs(this.middleExerciseList[i].start_time).format('YYYY-MM-DD HH:mm:ss')
                    this.middleExerciseList[i].end_time = this.dayjs(this.middleExerciseList[i].end_time).format('YYYY-MM-DD HH:mm:ss')
                    this.currentExerciseList.push(this.middleExerciseList[i])
                }
            },
            // 获取练习题
            async getExerciseList () {
                this.exerciseList = []
                this.middleExerciseList = []

                this.$http.get('/course/paper/', { params: { course_id: this.$store.state.currentCourseId } }).then(res => {
                    const exerciseList = res.data
                    // 进行中的卷子
                    const underWayList = []
                    // 已提交的卷子
                    const submittedList = []
                    // 已批改的卷子
                    const markedList = []
                    // 已结束的卷子
                    const finishedList = []
                    // 未开始的卷子
                    const notStartList = []

                    // 更新试卷状态
                    for (const item of exerciseList) {
                        if (new Date().getTime() < Date.parse(item.start_time)) {
                            item.student_status = 'NOTSTART'
                            notStartList.push(item)
                        } else if ((item.student_status === 'SUBMITTED' || item.student_status === 'MARKED') && new Date().getTime() >= Date.parse(item.start_time) && new Date().getTime() <= Date.parse(item.end_time)) {
                            item.student_status = 'REALSUBMITTED'
                            submittedList.push(item)
                        } else if (item.student_status === 'MARKED' && item.status === 'MARKED' && new Date().getTime() > Date.parse(item.end_time)) {
                            item.student_status = 'REALMARKED'
                            markedList.push(item)
                        } else if (new Date().getTime() >= Date.parse(item.start_time) && new Date().getTime() <= Date.parse(item.end_time)) {
                            item.student_status = 'UNDERWAY'
                            underWayList.push(item)
                        } else if (new Date().getTime() > Date.parse(item.end_time)) {
                            item.student_status = 'FINISHED'
                            finishedList.push(item)
                        }
                        // 章节过滤器
                        this.chapterStatusFilters.push({
                            text: item.chapter_name,
                            value: item.chapter_id
                        })
                    }
                    // 按照顺序形成试题列表
                    this.exerciseList.push(...underWayList)
                    this.exerciseList.push(...submittedList)
                    this.exerciseList.push(...markedList)
                    this.exerciseList.push(...finishedList)
                    this.exerciseList.push(...notStartList)
                    // 去除草稿试卷
                    this.exerciseList = this.exerciseList.filter(item => {
                        return item.status !== 'DRAFT'
                    })
                    this.middleExerciseList = this.exerciseList
                    this.pagination.count = this.middleExerciseList.length
                    // 去重函数
                    const trim = () => {
                        const map = new Map()
                        for (const item of this.chapterStatusFilters) {
                            if (!map.has(item.value)) {
                                map.set(item.value, item)
                            }
                        }
                        return [...map.values()]
                    }
                    this.chapterStatusFilters = trim()
                    this.updateCurrentExerciseList()
                })
            }
        }
    }
</script>

<style scoped>
.content {
    margin-top: 20px;
}
</style>
