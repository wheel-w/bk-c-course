<template>
    <div class="wrapper">
        <div class="header">
            <div class="header-left">
                <div class="header-item">
                    <span>章节：</span>
                    <bk-select v-model="chapter.chapterValue" :clearable="false" style="width: 100px">
                        <bk-option v-for="item in chapter.chapterList" :key="item.value" :id="item.value" :name="item.name">
                        </bk-option>
                    </bk-select>
                </div>
                <div class="header-item">
                    <span>状态：</span>
                    <bk-select v-model="type.typeValue" :clearable="false" style="width: 100px">
                        <bk-option v-for="item in type.typeList" :key="item.value" :id="item.value" :name="item.name">
                        </bk-option>
                    </bk-select>
                </div>
                <bk-button :theme="'primary'" @click="type.typeValue = 0; chapter.chapterValue = 1">
                    重置
                </bk-button>
            </div>
            <div class="header-right">
                <bk-button v-if="$store.state.user.identity === 'TEACHER'" @click="$store.state.user.identity = 'STUDENT'">切换为学生</bk-button>
                <bk-button v-else @click="$store.state.user.identity = 'TEACHER'">切换为老师</bk-button>
                <bk-search-select placeholder="请输入要查询的习题名称" style="width: 200px" v-model="searchText"
                    @key-enter="toSearch"
                    @search="toSearch">
                </bk-search-select>
            </div>
        </div>
        <div class="content">
            <bk-table :data="currentExerciseList"
                :size="'media'"
                max-height="500"
                :pagination="pagination"
                @page-change="handlePageChange"
                @page-limit-change="handlePageLimitChange">
                <bk-table-column type="index" label="序号" width="100"></bk-table-column>
                <bk-table-column label="习题名称" width="200">
                    <template slot-scope="props">
                        <div v-if="$store.state.user.identity === 'STUDENT'">
                            <bk-button v-if="new Date().getTime() < Date.parse(props.row.start_time)" theme="primary" text disabled>{{ props.row.paper_name }}</bk-button>
                            <bk-button v-if="new Date().getTime() >= Date.parse(props.row.start_time) && new Date().getTime() <= Date.parse(props.row.end_time)" theme="primary" text @click="toAnswer(props.row.id, false)">{{ props.row.paper_name }}</bk-button>
                            <bk-button v-if="new Date().getTime() > Date.parse(props.row.end_time) && props.row.status !== 'MARKED'" theme="primary" text disabled>{{ props.row.paper_name }}</bk-button>
                            <bk-button v-if="props.row.status === 'MARKED'" theme="primary" text @click="toAnalyze(props.row.id, true)">{{ props.row.paper_name }}</bk-button>
                        </div>
                        <div v-if="$store.state.user.identity === 'TEACHER'">
                            <bk-button text>{{ props.row.paper_name }}</bk-button>
                        </div>
                    </template>
                </bk-table-column>
                <bk-table-column label="开始时间" prop="start_time" width="200"></bk-table-column>
                <bk-table-column label="截止时间" prop="end_time" width="200"></bk-table-column>
                <bk-table-column label="我的分数" prop="score" width="150">
                    <template slot-scope="props">
                        {{ props.row.status === 'MARKED' ? props.row.score : '———' }}
                    </template>
                </bk-table-column>
                <bk-table-column label="习题状态" width="200">
                    <template slot-scope="props">
                        <bk-tag v-if="new Date().getTime() < Date.parse(props.row.start_time)" theme="danger" radius="10px" type="filled">未开始</bk-tag>
                        <bk-tag v-if="new Date().getTime() >= Date.parse(props.row.start_time) && new Date().getTime() <= Date.parse(props.row.end_time)" theme="success" radius="10px" type="filled">进行中</bk-tag>
                        <bk-tag v-if="new Date().getTime() > Date.parse(props.row.end_time) && props.row.status !== 'MARKED'" theme="warning" radius="10px" type="filled">待批改</bk-tag>
                        <bk-tag v-if="props.row.status === 'MARKED'" theme="info" radius="10px" type="filled">已完成</bk-tag>
                    </template>
                </bk-table-column>
                <bk-table-column label="操作">
                    <template slot-scope="props">
                        <div v-if="$store.state.user.identity === 'STUDENT'">
                            <bk-button v-if="new Date().getTime() < Date.parse(props.row.start_time)" theme="primary" text disabled>暂未开始</bk-button>
                            <bk-button v-if="new Date().getTime() >= Date.parse(props.row.start_time) && new Date().getTime() <= Date.parse(props.row.end_time)" theme="primary" text @click="toAnswer(props.row.id, false)">开始答题</bk-button>
                            <bk-button v-if="new Date().getTime() > Date.parse(props.row.end_time) && props.row.status !== 'MARKED'" theme="primary" text disabled>待批改</bk-button>
                            <bk-button v-if="props.row.status === 'MARKED'" theme="primary" text @click="toAnalyze(props.row.id, true)">查看解析</bk-button>
                        </div>
                        <div v-if="$store.state.user.identity === 'TEACHER'">
                            <bk-button v-if="new Date().getTime() > Date.parse(props.row.end_time)" theme="primary" text @click="toCorrect">批改试卷</bk-button>
                            <bk-button v-else theme="primary" text disabled>暂无试卷</bk-button>
                        </div>
                    </template>
                </bk-table-column>
            </bk-table>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'answer_question_index',
        data () {
            return {
                // 习题状态
                type: {
                    typeValue: 0,
                    typeList: [
                        {
                            name: '全部',
                            value: 0
                        },
                        {
                            name: '待完成',
                            value: 1
                        },
                        {
                            name: '已完成',
                            value: 2
                        }
                    ]
                },
                // 习题章节
                chapter: {
                    chapterValue: 1,
                    chapterList: [
                        {
                            name: '章节1',
                            value: 1
                        },
                        {
                            name: '章节2',
                            value: 2
                        },
                        {
                            name: '章节3',
                            value: 3
                        },
                        {
                            name: '章节4',
                            value: 4
                        }
                    ]
                },
                // 搜索语句
                searchText: '',
                // 总习题列表
                exerciseList: [],
                // 当前页习题列表
                currentExerciseList: [],
                // 分页器配置项
                pagination: {
                    current: 1,
                    count: 0,
                    limit: 10
                }
            }
        },
        watch: {
            // 监听当前课程id的变化
            '$store.state.currentCourseId' () {
                // 发送网络请求更新课程信息
                this.getExerciseList()
            },
            'type.typeValue' (newValue) {
                console.log(newValue)
            },
            'chapter.chapterValue' (newValue) {
                console.log(newValue)
            }
        },
        mounted () {
            console.log(this.$store.state.user)
            this.getExerciseList()
        },
        methods: {
            // 跳转答题页面
            toAnswer (id, isAccomplish) {
                this.$router.push({
                    name: 'answer_question_detail',
                    query: {
                        plan: 'private',
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
                        plan: 'private',
                        id,
                        isAccomplish
                    }
                })
            },
            // 跳转至试卷批改页面
            toCorrect (id) {
                this.$router.push({
                    name: 'correct_paper',
                    query: {
                        plan: 'private',
                        id
                    }
                })
            },
            // 监听搜索事件
            toSearch () {
                console.log(this.searchText)
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
                    this.currentExerciseList.push(this.exerciseList[i])
                }
                console.log(this.currentExerciseList)
            },
            // 获取练习题
            async getExerciseList () {
                this.$http.get('/course/paper/', { params: { course_id: this.$store.state.currentCourseId } }).then(res => {
                    this.exerciseList = res.data
                    this.pagination.count = this.exerciseList.length
                    this.updateCurrentExerciseList()
                })
            }
        }
    }
</script>

<style scoped>
.header {
    margin-top: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.header-left {
    flex: 0.4;
    display: flex;
    align-items: center;
    justify-content: space-around;
}
.header-right {
    display: flex;
    align-items: center;
    justify-content: space-around;
}
.header-item {
    display: flex;
    align-items: center;
}

.content {
    margin-top: 20px;
}
</style>
