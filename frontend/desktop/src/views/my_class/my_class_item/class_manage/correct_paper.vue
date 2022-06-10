<template>
    <div class="wrapper" v-if="paperEmpty">
        <bk-exception type="empty" scene="page">暂未要批改的试卷</bk-exception>
    </div>
    <div v-else class="wrapper" ref="top">
        <div class="header">
            <h2>试卷信息</h2>
            <bk-tag :theme="studentInfo.status === '已批改' ? 'success' : 'danger'" radius="10px" type="filled">{{ studentInfo.status === '已批改' ? '已批改' : '未批改' }}</bk-tag>
        </div>
        <div class="studentInfo">
            <span>学生id：{{ studentInfo.student_id }}</span>
            <span>学生姓名：{{ studentInfo.student_name }}</span>
            <span>答题时间：{{studentInfo.cumulative_time}}</span>
            <span>当前分数：{{ totalScore }}</span>
        </div>
        <div class="gradeCardContent">
            <div v-for="(item,index) in totalQuestion" :key="index">
                <div v-if="item.length !== 0">
                    <hr style="width: 80%; margin-left: 0">
                    <h3>第{{ index + 1 }}题</h3>
                    <h4>题目：【{{item.types}}】{{ item.title }}（{{item.score}}分）</h4>
                    <bk-radio-group v-if="item.types === '单选题'" class="radio-common" v-model="item.stu_answers">-->
                        <bk-radio value="A" :disabled="true">
                            A：{{ item.option_A }}
                        </bk-radio>
                        <bk-radio value="B" :disabled="true">
                            B：{{ item.option_B }}
                        </bk-radio>
                        <bk-radio value="C" :disabled="true">
                            C：{{ item.option_C }}
                        </bk-radio>
                        <bk-radio value="D" :disabled="true">
                            D：{{ item.option_D }}
                        </bk-radio>
                    </bk-radio-group>
                    <bk-checkbox-group v-else-if="item.types === '多选题'" class="radio-common" v-model="item.stu_answers">
                        <bk-checkbox value="A" :disabled="true">
                            A：{{ item.option_A }}
                        </bk-checkbox>
                        <bk-checkbox value="B" :disabled="true">
                            B：{{ item.option_B }}
                        </bk-checkbox>
                        <bk-checkbox value="C" :disabled="true">
                            C：{{ item.option_C }}
                        </bk-checkbox>
                        <bk-checkbox value="D" :disabled="true">
                            D：{{ item.option_D }}
                        </bk-checkbox>
                        <bk-checkbox value="E" :disabled="true">
                            E：{{ item.option_E }}
                        </bk-checkbox>
                    </bk-checkbox-group>
                    <bk-radio-group v-else-if="item.types === '判断题'" class="radio-common" v-model="item.stu_answers">
                        <bk-radio value="T" :disabled="true">
                            T：{{ item.option_A }}
                        </bk-radio>
                        <bk-radio value="F" :disabled="true">
                            F：{{ item.option_B }}
                        </bk-radio>
                    </bk-radio-group>
                    <div>
                        <bk-tag theme="info">学生答案：{{item.stu_answers}}</bk-tag>
                        <bk-tag theme="success"><span>正确答案：</span>{{item.answer}}</bk-tag>
                    </div>
                    <div style="margin-top: 10px">
                        请选择该题得分：<bk-input type="number" style="width: 110px" v-model="item.stu_score" :max="item.score" :min="0"></bk-input>
                    </div>
                </div>
            </div>
        </div>
        <bk-button style="width: 120px;position: fixed; bottom: 220px; right: 6%;border-radius: 20px;" :theme="'primary'" type="submit" @click="toPreStudent">上一个</bk-button>
        <bk-button style="width: 120px;position: fixed; bottom: 170px; right: 6%;border-radius: 20px;" :theme="'primary'" type="submit" @click="toNextStudent">下一个</bk-button>
        <bk-button style="width: 120px;position: fixed; bottom: 120px; right: 6%;border-radius: 20px;" :theme="studentInfo.status === 'MARKED' ? 'warning' : 'success'" type="submit" @click="checkAnswer">{{ studentInfo.status === '已批改' ? '重新批改' : '确认批改' }}</bk-button>

        <bk-button style="width: 120px;position: fixed; bottom: 270px; right: 6%;border-radius: 20px;" @click="gradeCard.visible = true" :theme="'success'" :outline="true">
            展开批改情况
        </bk-button>
        <bk-dialog v-model="gradeCard.visible"
            width="720"
            :position="gradeCard.position"
            title="批改卡"
            :show-footer="false">
            <div class="gradeCardContent">
                <h3>已提交</h3>
                <div style="display: flex;flex-wrap: wrap;">
                    <div v-for="(item,index) in studentInfoList" :key="item.student_id">
                        <bk-button style="margin-left: 10px; margin-bottom: 10px; width: 110px; height: 40px; font-size: 18px; border-radius: 5px; overflow: hidden; text-overflow: ellipsis;" :theme="item.status === '已批改' ? 'success' : 'primary'" @click="chooseStudent(index)">{{ item.student_name === null ? item.student_id : item.student_name }}</bk-button>
                    </div>
                </div>
                <h3>未提交</h3>
                <div style="display: flex;flex-wrap: wrap;">
                    <div v-for="item in notSubmittedStudentList" :key="item.student_id">
                        <bk-button style="margin-left: 10px; margin-bottom: 10px; width: 110px; height: 40px; font-size: 18px; border-radius: 5px; overflow: hidden; text-overflow: ellipsis;" :theme="'danger'" disabled>{{ item.student_name === null ? item.student_id : item.student_name }}</bk-button>
                    </div>
                </div>
            </div>
        </bk-dialog>
    </div>
</template>

<script>
    export default {
        name: 'correct_paper',
        data () {
            return {
                paperEmpty: false, // 是否拥有可批改的试卷
                currentPaperId: 0, // 当前试卷id
                currentConcatId: 0, // 当前批改学生卷子id
                currentStuAnswer: [], // 当前学生卷子答案
                totalQuestion: {}, // 习题列表
                // 批改上传uploadData参数
                uploadData: {
                    student_answer_list: [],
                    student_paper_contact_id: 0
                },
                currentStudentIndex: 0, // 当前学生index
                studentInfo: {}, // 当前批改学生信息
                studentInfoList: [], // 所有提交试卷的学生信息
                notSubmittedStudentList: [], // 所以未提交试卷的学生信息
                gradeCard: {
                    visible: false,
                    position: {
                        top: 100
                    }
                },
                totalScore: 0,
                score_list: []
            }
        },
        computed: {
            // 展示当前分数
            // totalScore () {
            //     let score = 0
            //     for (const item in this.totalQuestion) {
            //         for (const childItem of this.totalQuestion[item]) {
            //             score += parseInt(childItem.student_score)
            //         }
            //     }
            //     return score
            // }
        },
        watch: {
            // 监听当前课程id的变化
            '$store.state.currentCourseId' () {
                this.$router.replace({
                    name: 'displaypaper'
                })
            }
        },
        mounted () {
            this.currentPaperId = this.$route.query.paperId
            this.currentPaperEndTime = Date.parse(this.$route.query.endTime)
            this.getQuestionList()
        },
        methods: {
            // 获取当前学生做答题目列表
            async getStudentQuestionStation () {
                console.log('totalQuestion', this.totalQuestion)
                this.$http.get(`/api/project-task-info/${this.currentPaperId}/stu-info/${this.currentConcatId}/`).then(res => {
                    console.log('学生试卷详情', res)
                    this.studentInfo.cumulative_time = res.data.cumulative_time
                    this.studentInfo.status = res.data.status
                    console.log('this.studentInfo', this.studentInfo)
                    this.currentStuAnswer = res.data.stu_answers
                    this.totalScore = res.data.total_score
                    for (const item in this.totalQuestion) {
                        this.totalQuestion[item].stu_answers = ''
                        this.totalQuestion[item].stu_score = 0
                    }
                    for (const i in this.currentStuAnswer) {
                        this.totalQuestion[i].stu_answers = this.currentStuAnswer[i]
                    }
                })
            },
            // 学生答题信息和学生做答题目列表
            getQuestionList () {
                this.$http.get(`/api/project-task/${this.currentPaperId}/teacher/`).then(res => {
                    console.log(res)
                    this.totalQuestion = res.data.questions_info
                    this.notSubmittedStudentList = res.data.student_info
                    this.studentInfoList = res.data.submitted_student_info
                    // this.notSubmittedStudentList = this.notSubmittedStudentList.pop(this.studentInfoList)
                    for (const i in this.studentInfoList) {
                        const studentId = this.studentInfoList[i].student_id
                        // 在所有学生列表中删除掉已经提交的学生名单就是未提交的学生名单
                        this.notSubmittedStudentList = this.notSubmittedStudentList.filter((item) => {
                            return item.student_id !== studentId
                        })
                    }
                    console.log('this.notSubmittedStudentList', this.notSubmittedStudentList)
                    // 根据卷子结束时间添加要批改的学生列表
                    // if (new Date().getTime() > this.currentPaperEndTime) {
                    //     this.studentInfoList = res.data.submitted_student_info.filter(item => {
                    //         return item.status === 'SUBMITTED' || item.status === 'MARKED' || item.status === 'SAVED'
                    //     })
                    // } else {
                    //     this.studentInfoList = res.data.submitted.filter(item => {
                    //         return item.status === 'SUBMITTED' || item.status === 'MARKED'
                    //     })
                    // }
                    // 为空时候代表无卷子需要批改
                    if (this.studentInfoList.length === 0) {
                        this.paperEmpty = true
                        return
                    }
                    this.studentInfo = this.studentInfoList[0]
                    this.currentStudentIndex = 0
                    this.currentConcatId = this.studentInfo.student_id
                    this.getStudentQuestionStation()
                })
            },
            // 发起批改试卷请求
            checkAnswer () {
                this.score_list = []
                this.totalQuestion.forEach(e => {
                    this.score_list.push(e.stu_score)
                })
                this.$http.patch(`/api/project-task-info/${this.currentPaperId}/judge/${this.currentConcatId}/`, { data: { 'score_list': this.score_list } }).then(res => {
                    console.log('批改试卷res', res)
                    if (res.message === 'success') {
                        this.$bkMessage({
                            message: '批改成功！',
                            theme: 'success'
                        })
                        // 更新批改状态
                        this.getQuestionList()
                    } else {
                        this.$bkMessage({
                            message: '批改失败！',
                            theme: 'error'
                        })
                    }
                })
                this.toTop()
            },
            // 下一个学生试卷
            async toNextStudent () {
                if (this.currentStudentIndex + 1 >= this.studentInfoList.length) {
                    this.$bkMessage({
                        message: '已经是最后一个学生啦！',
                        theme: 'warning'
                    })
                } else {
                    this.currentStudentIndex++
                    this.studentInfo = this.studentInfoList[this.currentStudentIndex]
                    this.getStudentQuestionStation()
                    this.toTop()
                }
            },
            // 上一个学生试卷
            async toPreStudent () {
                if (this.currentStudentIndex - 1 < 0) {
                    this.$bkMessage({
                        message: '前面没有学生啦！',
                        theme: 'warning'
                    })
                } else {
                    this.currentStudentIndex--
                    this.studentInfo = this.studentInfoList[this.currentStudentIndex]
                    this.getStudentQuestionStation()
                    this.toTop()
                }
            },
            // 选择任一学生试卷
            async chooseStudent (index) {
                this.currentStudentIndex = index
                this.studentInfo = this.studentInfoList[this.currentStudentIndex]
                await this.getStudentQuestionStation()
                this.toTop()
                this.gradeCard.visible = false
            },
            // 返回顶部
            toTop () {
                this.$refs.top.scrollTop = 0
            }
        }
    }
</script>

<style scoped>
.wrapper {
    display: flex;
    flex-direction: column;
    height: 580px;
    overflow-y: auto;
}

.header {
    display: flex;
    align-items: center;
}

.radio-common {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    box-shadow: none;
    margin-bottom: 20px;
}
.radio-common .bk-form-radio, .radio-common .bk-form-checkbox{
    margin: 5px;
}

.studentInfo {
    margin-left: 0px;
    /*display: flex;*/
    /*align-items: center;*/
    /*justify-content: space-around;*/
}
.studentInfo span{
    margin-right: 100px;
}

.gradeCardContent {
    height: 500px;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
}
.gradeCardContent::-webkit-scrollbar {
    /*滚动条整体样式*/
    width: 5px;  /*高宽分别对应横竖滚动条的尺寸*/
    height: 1px;
}
.gradeCardContent::-webkit-scrollbar-thumb {
    /*滚动条里面小方块*/
    border-radius: 10px;
    box-shadow: inset 0 0 5px rgb(255, 255, 255);
    background: #868686;
}
.gradeCardContent::-webkit-scrollbar-track {
    /*滚动条里面轨道*/
    box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
    border-radius: 10px;
    background: #ededed;
}
</style>
