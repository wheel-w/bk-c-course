<template>
    <div class="wrapper" v-if="paperEmpty">
        <bk-exception type="empty" scene="page">暂未要批改的试卷</bk-exception>
    </div>
    <div v-else class="wrapper" ref="top">
        <div class="header">
            <h2>试卷信息</h2>
            <bk-tag :theme="studentInfo.status === 'MARKED' ? 'success' : 'danger'" radius="10px" type="filled">{{ studentInfo.status === 'MARKED' ? '已批改' : '未批改' }}</bk-tag>
        </div>
        <div class="studentInfo">
            <span>学生班级：{{ studentInfo.class === null ? '未认证班级' : studentInfo.class }}</span>
            <span>学生姓名：{{ studentInfo.name === null ? '未认证姓名' : studentInfo.name }}</span>
            <span>学生学号：{{ studentInfo.class_number }}</span>
            <span>当前分数：{{ totalScore }}</span>
        </div>

        <div v-for="(item,index) in totalQuestion" :key="index">
            <div v-if="item.length !== 0">
                <h3>{{ index }}</h3>
                <bk-card class="radio-common" :title="`${childIndex + 1}.${childItem.question} （${childItem.score}分）`" v-for="(childItem,childIndex) in item" :key="childIndex" :border="false">
                    <bk-radio-group v-if="childItem.types === 'SINGLE'" class="radio-common" v-model="childItem.student_answer">
                        <bk-radio value="A" :disabled="true">
                            A：{{ childItem.option_A }}
                        </bk-radio>
                        <bk-radio value="B" :disabled="true">
                            B：{{ childItem.option_B }}
                        </bk-radio>
                        <bk-radio value="C" :disabled="true">
                            C：{{ childItem.option_C }}
                        </bk-radio>
                        <bk-radio value="D" :disabled="true">
                            D：{{ childItem.option_D }}
                        </bk-radio>
                    </bk-radio-group>
                    <bk-checkbox-group v-if="childItem.types === 'MULTIPLE'" class="radio-common" v-model="childItem.student_answer">
                        <bk-checkbox value="A" :disabled="true">
                            A：{{ childItem.option_A }}
                        </bk-checkbox>
                        <bk-checkbox value="B" :disabled="true">
                            B：{{ childItem.option_B }}
                        </bk-checkbox>
                        <bk-checkbox value="C" :disabled="true">
                            C：{{ childItem.option_C }}
                        </bk-checkbox>
                        <bk-checkbox value="D" :disabled="true">
                            D：{{ childItem.option_D }}
                        </bk-checkbox>
                        <bk-checkbox value="E" :disabled="true">
                            E：{{ childItem.option_E }}
                        </bk-checkbox>
                    </bk-checkbox-group>
                    <div style="margin-top: 10px">
                        学生答案：<span>{{ childItem.student_answer }}</span>
                    </div>
                    <div style="margin-top: 10px">
                        正确答案为：
                        <span v-if="childItem.types === 'JUDGE'">{{ item.answer === 'false' ? 'F' : 'T' }}</span>
                        <span v-else>{{ childItem.answer }}</span>
                    </div>
                    <div style="margin-top: 10px">
                        打分：<bk-input type="number" style="width: 110px" v-model="childItem.student_score" :max="childItem.score" :min="0"></bk-input>
                    </div>
                </bk-card>
            </div>
        </div>

        <bk-button style="width: 120px;position: fixed; bottom: 220px; right: 6%;border-radius: 20px;" :theme="'primary'" type="submit" @click="toPreStudent">上一个</bk-button>
        <bk-button style="width: 120px;position: fixed; bottom: 170px; right: 6%;border-radius: 20px;" :theme="'primary'" type="submit" @click="toNextStudent">下一个</bk-button>
        <bk-button style="width: 120px;position: fixed; bottom: 120px; right: 6%;border-radius: 20px;" :theme="studentInfo.status === 'MARKED' ? 'warning' : 'success'" type="submit" @click="checkAnswer">{{ studentInfo.status === 'MARKED' ? '重新批改' : '确认批改' }}</bk-button>

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
                        <bk-button style="margin-left: 10px; margin-bottom: 10px; width: 110px; height: 40px; font-size: 18px; border-radius: 5px; overflow: hidden; text-overflow: ellipsis;" :theme="item.status === 'MARKED' ? 'success' : 'default'" @click="chooseStudent(index)">{{ item.name === null ? item.student_id : item.name }}</bk-button>
                    </div>
                </div>
                <h3>未提交</h3>
                <div style="display: flex;flex-wrap: wrap;">
                    <div v-for="item in notSubmittedStudentList" :key="item.student_id">
                        <bk-button style="margin-left: 10px; margin-bottom: 10px; width: 110px; height: 40px; font-size: 18px; border-radius: 5px; overflow: hidden; text-overflow: ellipsis;" theme="danger" disabled>{{ item.name === null ? item.student_id : item.name }}</bk-button>
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
                }
            }
        },
        computed: {
            // 展示当前分数
            totalScore () {
                let score = 0
                for (const item in this.totalQuestion) {
                    for (const childItem of this.totalQuestion[item]) {
                        score += parseInt(childItem.student_score)
                    }
                }
                return score
            }
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
            this.currentPaperId = this.$route.query.paperid
            this.currentPaperEndTime = Date.parse(this.$route.query.endTime)
            this.getQuestionList()
        },
        methods: {
            // 获取当前学生做答题目列表
            async getStudentQuestionStation () {
                this.$http.get('/course/mark_or_check_paper/', { params: { course_id: this.$store.state.currentCourseId, paper_id: this.currentPaperId, student_id: this.studentInfo.student_id } }).then(res => {
                    this.currentConcatId = res.data.StudentPaperContact_id
                    this.totalQuestion = res.data
                    delete this.totalQuestion['StudentPaperContact_id']
                    delete this.totalQuestion['total_score']
                    for (const item in this.totalQuestion) {
                        for (const childItem of this.totalQuestion[item]) {
                            if (childItem.student_answer === null) {
                                childItem.student_answer = '未作答'
                            }
                        }
                    }
                })
            },
            // 学生答题信息和学生做答题目列表
            getQuestionList () {
                this.$http.get('/course/get_student_answer_info/', { params: { course_id: this.$store.state.currentCourseId, paper_id: this.currentPaperId } }).then(res => {
                    this.notSubmittedStudentList = res.data.not_submitted
                    // 根据卷子结束时间添加要批改的学生列表
                    if (new Date().getTime() > this.currentPaperEndTime) {
                        this.studentInfoList = res.data.submitted.filter(item => {
                            return item.status === 'SUBMITTED' || item.status === 'MARKED' || item.status === 'SAVED'
                        })
                    } else {
                        this.studentInfoList = res.data.submitted.filter(item => {
                            return item.status === 'SUBMITTED' || item.status === 'MARKED'
                        })
                    }
                    // 为空时候代表无卷子需要批改
                    if (this.studentInfoList.length === 0) {
                        this.paperEmpty = true
                        return
                    }
                    this.studentInfo = this.studentInfoList[0]
                    this.currentStudentIndex = 0
                    this.getStudentQuestionStation()
                })
            },
            // 发起批改试卷请求
            async checkAnswer () {
                this.uploadData = {
                    student_answer_list: [],
                    student_paper_contact_id: this.currentConcatId,
                    course_id: this.$store.state.currentCourseId
                }
                for (const item in this.totalQuestion) {
                    for (const childItem of this.totalQuestion[item]) {
                        this.uploadData.student_answer_list.push(
                            {
                                id: childItem.student_answer_id,
                                score: parseInt(childItem.student_score)
                            }
                        )
                    }
                }
                this.$http.post('/course/teacher_correct_paper/', this.uploadData).then(res => {
                    if (res.code === 200) {
                        this.$bkMessage({
                            message: '批改成功',
                            theme: 'success'
                        })
                        // 更新批改状态
                        this.$http.get('/course/get_student_answer_info/', { params: { course_id: this.$store.state.currentCourseId, paper_id: this.currentPaperId } }).then(res => {
                            this.notSubmittedStudentList = res.data.not_submitted
                            // 根据卷子结束时间添加要批改的学生列表
                            if (new Date().getTime() > this.currentPaperEndTime) {
                                this.studentInfoList = res.data.submitted.filter(item => {
                                    return item.status === 'SUBMITTED' || item.status === 'MARKED' || item.status === 'SAVED'
                                })
                            } else {
                                this.studentInfoList = res.data.submitted.filter(item => {
                                    return item.status === 'SUBMITTED' || item.status === 'MARKED'
                                })
                            }
                            this.studentInfo = this.studentInfoList[this.currentStudentIndex]
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
                this.getStudentQuestionStation()
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
}

.studentInfo {
    display: flex;
    align-items: center;
    justify-content: space-around;
}

.gradeCardContent {
    height: 500px;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
}
</style>
