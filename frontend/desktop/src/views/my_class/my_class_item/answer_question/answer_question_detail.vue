<template>
    <div class="myWrapper" v-if="$route.query.isAccomplish" ref="top">
        <div class="header" v-if="$route.query.isMarked">
            <h2>总分：{{ totalScore === null ? '————' : totalScore }}</h2>
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
                    <div v-if="childItem.types === 'SINGLE' || childItem.types === 'MULTIPLE'">
                        <bk-divider></bk-divider>
                    </div>
                    <div style="margin-top: 10px">
                        你的答案：<span>{{ childItem.student_answer }}</span>
                    </div>
                    <div style="margin-top: 10px" v-if="$route.query.isMarked">
                        正确答案为：
                        <span v-if="childItem.types === 'JUDGE'">{{ item.answer === 'false' ? 'F' : 'T' }}</span>
                        <span v-else>{{ childItem.answer }}</span>
                    </div>
                    <div style="margin-top: 10px" v-if="$route.query.isMarked">
                        解析：<span>{{ childItem.explain === null ? '暂无解析' : childItem.explain}}</span>
                    </div>
                    <div style="margin-top: 10px" v-if="$route.query.isMarked">
                        得分：{{ childItem.student_score === null ? 0 : childItem.student_score }}
                    </div>
                </bk-card>
            </div>
        </div>

        <bk-button @click="$refs.top.scrollTop = 0" style="width: 120px;position: fixed; bottom: 120px; right: 6%;border-radius: 20px;" :theme="'primary'">
            返回顶部
        </bk-button>
    </div>
    <div class="wrapper" v-else>
        <div class="progress">
            <div>
                <bk-icon type="clock" />
                累计答题时间：{{count}}
            </div>
        </div>
        <div class="answer_sheet">
            <h3>答题卡</h3>
            <ul id="answer_sheet_number">
                <li v-for="item in questionsInfo" :key="item.index">
                    <bk-button v-if="(item.stu_answers === '') || (item.stu_answers === null) || (item.stu_answers === '[]')" :theme="'primary'" type="submit" class="mr10 switchQuestion" size="small" @click="selectQuestion(item.index)">{{item.index}}</bk-button>
                    <bk-button v-else-if="(item.stu_answers !== '') && (item.stu_answers !== null) && (item.stu_answers !== '[]')" :theme="'success'" type="submit" class="mr10 switchQuestion" size="small" @click="selectQuestion(item.index)">{{item.index}}</bk-button>
                </li>
            </ul>
            <div class="answer_sheet_explain">
                <hr>
                <div class="answer_explain_button">
                    <bk-button :theme="'primary'" type="submit" class="mr10">
                        未完成
                    </bk-button>
                    <bk-button :theme="'success'" type="submit" class="mr10">
                        已完成
                    </bk-button>
                </div>
            </div>
        </div>
        <div class="answer">
            <h3>请在此处答题</h3>
            <div class="answer_area">
                <bk-button :theme="'default'" icon="angle-left" class="last mr10" @click="lastQuestion"></bk-button>
                <div class="question_box">
                    <ul class="question_lists">
                        <li class="question_item" v-for="item in questionsInfo" :key="item.index">{{item.index}}.【{{item.types}}】{{item.title}}（{{item.score}}分）
                            <div v-if="item.types === '单选题'">
                                <bk-radio-group v-model="item.stu_answers">
                                    <bk-radio :value="'A'">
                                        A. {{item.option_A}}
                                    </bk-radio>
                                    <br>
                                    <bk-radio :value="'B'">
                                        B. {{item.option_B}}
                                    </bk-radio>
                                    <br>
                                    <bk-radio :value="'C'">
                                        C. {{item.option_C}}
                                    </bk-radio>
                                    <br>
                                    <bk-radio :value="'D'">
                                        D. {{item.option_D}}
                                    </bk-radio>
                                    <br>
                                </bk-radio-group>
                                <p class="mb5">我的答案：{{item.stu_answers}}</p>
                            </div>
                            <div v-else-if="item.types === '多选题'">
                                <bk-checkbox-group v-model="item.stu_answers">
                                    <bk-checkbox :value="'A'">A. {{item.option_A}}</bk-checkbox>
                                    <br>
                                    <bk-checkbox :value="'B'">B. {{item.option_B}}</bk-checkbox>
                                    <br>
                                    <bk-checkbox :value="'C'">C. {{item.option_C}}</bk-checkbox>
                                    <br>
                                    <bk-checkbox :value="'D'">D. {{item.option_D}}</bk-checkbox>
                                    <br>
                                    <bk-checkbox :value="'E'">E. {{item.option_E}}</bk-checkbox>
                                    <br>
                                </bk-checkbox-group>
                                <p class="mb5">我的答案：{{item.stu_answers}}</p>
                            </div>
                            <div v-else-if="item.types === '判断题'">
                                <bk-radio-group v-model="item.stu_answers">
                                    <bk-radio :value="'T'">
                                        T. 正确
                                    </bk-radio>
                                    <br>
                                    <bk-radio :value="'F'">
                                        F. 错误
                                    </bk-radio>
                                    <br>
                                </bk-radio-group>
                                <p class="mb5">我的答案：{{item.stu_answers}}</p>
                            </div>
                            <div v-else-if="item.types === '简答题'">
                                <div class="input-answer">
                                    <bk-input placeholder="请输入你的答案" :type="'textarea'" :rows="3" :maxlength="255"
                                        v-model="item.stu_answers">
                                    </bk-input>
                                </div>
                                <p class="mb5">我的答案：{{item.stu_answers}}</p>
                            </div>
                            <div v-else-if="item.types === 'SHORT_ANSWER'">
                                <div class="input-answer">
                                    <bk-input placeholder="请输入你的答案" :type="'textarea'" :rows="3" :maxlength="255"
                                        v-model="item.stu_answers">
                                    </bk-input>
                                </div>
                                <p class="mb5">我的答案：{{item.stud_answers}}</p>
                            </div>
                        </li>
                    </ul>
                </div>
                <bk-button :theme="'default'" icon="angle-right" class="next" @click="nextQuestion"></bk-button>
            </div>
            <div class="answer_submit">
                <hr>
                <div class="answer_submit_button">
                    <bk-button :theme="'primary'" type="submit" :title="'基础按钮'" @click="clickSavaAnswer" class="mr10">
                        保存
                    </bk-button>
                    <bk-button :theme="'primary'" ref="submit" :disabled="disabled" type="submit" :title="'基础按钮'" @click="clickSubmit" class="mr10">
                        提交
                    </bk-button>
                </div>
            </div>
        </div>
        <div class="dialog">
            <!--保存Dialog-->
            <bk-dialog v-model="saveAnswerDialog.primary.visible"
                theme="primary"
                :mask-close="false"
                :header-position="saveAnswerDialog.primary.headerPosition"
                @confirm="saveAnswer"
                title="保存答案">
                <h3>确认要保存当前作答？</h3>
            </bk-dialog>
            <!--提交Dialog-->
            <bk-dialog v-model="submitAnswerDialog.primary.visible"
                theme="primary"
                :mask-close="false"
                :header-position="submitAnswerDialog.primary.headerPosition"
                @confirm="submitAnswer"
                title="提交试卷">
                <h3>确认要提交当前试卷？</h3>
            </bk-dialog>
        </div>
    </div>
    
</template>

<script>
    export default {
        name: 'answer_question_detail',
        data () {
            return {
                totalQuestion: {}, // 总习题列表
                totalScore: 0, // 总分
                disabled: false,
                count: '', // 计时
                seconds: 0, // 从0秒开始计数
                msg: '',
                answer_info: [],
                paper_id: 0,
                questionsInfo: [],
                stu_answers: [],
                answer: [],
                saveAnswerDialog: {
                    primary: {
                        visible: false,
                        headerPosition: 'left'
                    }
                },
                submitAnswerDialog: {
                    primary: {
                        visible: false,
                        headerPosition: 'left'
                    }
                }
            }
        },
        watch: {
            // 监听当前课程id的变化
            '$store.state.currentCourseId' () {
                this.$router.replace({
                    name: 'answer_question_index'
                })
            }
        },
        mounted () {
            this.paper_id = this.$route.query.id
            this.project_id = this.$route.query.project_id
            if (this.$route.query.isAccomplish) {
                this.getStudentQuestionList()
            } else {
                this.Time() // 调用定时器
                this.getPaperStatus() // 调用试卷状态
                const that = this
                setTimeout(function () {
                    that.submitButtonDisabled()
                }, 2000)
            }
            // this.getQuestionList()
        },
        methods: {
            // 获取问题列表
            // async getStudentQuestionList () {
            //     this.$http.get('/course/answer_or_check_paper/', { params: { paper_id: this.paper_id } }).then(res => {
            //         this.totalQuestion = res.data
            //         this.totalScore = res.data.total_score
            //         delete this.totalQuestion['total_score']
            //         delete this.totalQuestion['cumulative_time']
            //         delete this.totalQuestion['status']
            //         for (const item in this.totalQuestion) {
            //             for (const childItem of this.totalQuestion[item]) {
            //                 if (childItem.student_answer === null) {
            //                     childItem.student_answer = '未作答'
            //                 }
            //             }
            //         }
            //     })
            // },
            // 时 分 秒 格式化函数
            countUp () {
                let h = parseInt(this.seconds / (60 * 60) % 24)
                h = h < 10 ? '0' + h : h
                let m = parseInt(this.seconds / 60 % 60)
                m = m < 10 ? '0' + m : m
                let s = parseInt(this.seconds % 60)
                s = s < 10 ? '0' + s : s
                this.count = h + '时' + m + '分' + s + '秒'
            },
            // 定时器没过1秒参数加1
            Time () {
                setInterval(() => {
                    this.seconds += 1
                    this.countUp()
                    this.submitButtonDisabled()
                }, 1000)
            },
            clickSavaAnswer () {
                this.saveAnswerDialog.primary.visible = true
            },
            saveAnswer () {
                this.stu_answers = []
                this.questionsInfo.forEach(e => {
                    this.stu_answers.push(e.stu_answers)
                })
                for (let i = 0; i < this.stu_answers.length; i++) {
                    if (this.stu_answers[i] === '') {
                        this.stu_answers[i] = 'HAS_NOT_SOLVED'
                    }
                }
                for (const i in this.stu_answers) {
                    if (this.stu_answers[i].constructor === Array) {
                        this.stu_answers[i] = this.stu_answers[i].join('')
                    }
                }
                console.log('this.stu_answers', this.stu_answers)
                this.$http.patch(`/api/project-task-info/${this.paper_id}/`, { 'stu_answers': this.stu_answers, 'status': 'SAVED', 'cumulative_time': this.seconds }).then(res => {
                    console.log('save的res', res)
                    if (res.result === true) {
                        this.$bkMessage({
                            message: '保存成功',
                            theme: 'success'
                        })
                        this.toAnswerQuestionIndex()
                    } else {
                        this.$bkMessage({
                            message: '保存失败',
                            theme: 'error'
                        })
                    }
                })
            },
            clickSubmit () {
                this.submitAnswerDialog.primary.visible = true
            },
            submitAnswer () {
                this.stu_answers = []
                this.questionsInfo.forEach(e => {
                    this.stu_answers.push(e.stu_answers)
                })
                for (let i = 0; i < this.stu_answers.length; i++) {
                    if (this.stu_answers[i] === '' || this.stu_answers === []) {
                        this.stu_answers[i] = 'HAS_NOT_SOLVED'
                    }
                }
                for (const i in this.stu_answers) {
                    if (this.stu_answers[i].constructor === Array) {
                        this.stu_answers[i] = this.stu_answers[i].join('')
                    }
                }
                this.$http.patch(`/api/project-task-info/${this.paper_id}/`, { 'stu_answers': this.stu_answers, 'status': 'SUBMITTED', 'cumulative_time': this.seconds }).then(res => {
                    console.log('提交后res', res)
                    if (res.result === true) {
                        this.$bkMessage({
                            message: '提交成功',
                            theme: 'success'
                        })
                        this.toAnswerQuestionIndex()
                    } else {
                        this.$bkMessage({
                            message: '提交失败',
                            theme: 'error'
                        })
                    }
                })
            },
            toAnswerQuestionIndex () {
                setTimeout(() => {
                    this.$router.push({
                        name: 'answer_question_index',
                        params: {
                            'projectId': this.project_id
                        }
                    })
                }, 100)
            },
            lastQuestion () {
                const ul = document.querySelector('.question_lists')
                const li = document.querySelectorAll('.question_item')
                const liLength = li.length
                const liHeight = li[0].offsetHeight
                const relativeHeight = liLength * liHeight
                ul.style.width = relativeHeight + 'px'
                let ulTop = ul.offsetTop
                if (-(ulTop) > 0 && ulTop < relativeHeight * 4) {
                    ulTop = ulTop + liHeight
                    ul.style.top = ulTop + 'px'
                }
            },
            nextQuestion () {
                const ul = document.querySelector('.question_lists')
                const li = document.querySelectorAll('.question_item')
                const liLength = li.length
                const liHeight = li[0].offsetHeight
                const relativeHeight = liLength * liHeight
                ul.style.height = liLength * liHeight + 'px'
                let ulTop = ul.offsetTop
                if (-(ulTop) < relativeHeight - 280) {
                    ulTop = ulTop - liHeight
                    ul.style.top = ulTop + 'px'
                }
            },
            selectQuestion (num) {
                const ul = document.querySelector('.question_lists')
                const li = document.querySelectorAll('.question_item')
                let currentnum = this.questionsInfo[0].index
                const liheight = li[0].offsetHeight
                let ultop = ul.offsetTop
                ultop = (currentnum - num) * liheight
                ul.style.top = ultop + 'px'
                currentnum = num
            },
            getPaperStatus () {
                console.log('获取试卷状态')
                this.$http.get(`/api/project-task/${this.paper_id}/student/`).then(res => {
                    console.log(res)
                    if (res.data.status === '已发布') {
                        this.getQuestionDetail()
                        // this.getQuestionList()
                    } else if (res.data.status === '草稿') {
                        this.$bkMessage({
                            message: '当前试卷未发布',
                            theme: 'error'
                        })
                        this.toAnswerQuestionIndex()
                    }
                })
            },
            // 获取学生自己的任务答题详情
            getQuestionDetail () {
                this.$http.get(`api/project-task-info/${this.paper_id}/`).then(res => {
                    console.log('获取详情', res)
                    if (res.data.status === '已保存' || res.data.status === '未答题') {
                        this.seconds = res.data.cumulative_time_seconds
                        this.answer = res.data.stu_answers
                        this.getQuestionList()
                    } else {
                        // this.seconds = 0
                        this.$bkMessage({
                            message: '该试卷已提交！',
                            theme: 'warning'
                        })
                        this.toAnswerQuestionIndex()
                    }
                })
            },
            // 获取问题列表
            getQuestionList () {
                this.$http.get(`/api/project-task/${this.paper_id}/student/`).then(res => {
                    this.questionsInfo = res.data.questions_info
                    console.log('this.questionInfo', this.questionsInfo)
                    for (const item in this.questionsInfo) {
                        this.questionsInfo[item].stu_answers = ''
                    }
                    for (const i in this.answer) {
                        this.questionsInfo[i].stu_answers = this.answer[i]
                    }
                    for (const items in this.questionsInfo) {
                        if (this.questionsInfo[items].stu_answers === 'HAS_NOT_SOLVED') {
                            this.questionsInfo[items].stu_answers = ''
                        }
                    }
                    console.log('this.questionsInfo:', this.questionsInfo)
                })
            },
            submitButtonDisabled () {
                // 判断是否存在没有做完的题目
                const someResult = this.questionsInfo.some(function (item) {
                    return item.stu_answers === '' || item.stu_answers === null || item.stu_answers === '[]'
                })
                // 如果题目没有做完，提交按钮禁用
                if (someResult === true) {
                    this.disabled = true
                } else if (someResult === false) {
                    this.disabled = false
                }
            }
        }
    }
</script>

<style scoped>
.myWrapper {
    display: flex;
    flex-direction: column;
    height: 580px;
    overflow-y: auto;
}

.radio-common {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    box-shadow: none;
}

.answer {
        width: 65%;
        float: right;
    }
    .bk-form-radio {
        margin-top: 20px;
    }
    .bk-form-checkbox {
        margin-top: 20px;
    }
    .mb5 {
        margin-top: 20px;
    }
    .input-answer {
        margin-top: 20px;
        width: 500px;
    }
    .bk-page {
        margin-top: 30px;
    }
    .answer_sheet {
        width: 30%;
        float: left;
        height: 400px;
        border: 1px solid #888888;
        border-radius: 7px;
    }
    .answer_sheet h3 {
        text-align: center;
    }
    #answer_sheet_number{
        margin-left: 20px;
        overflow: auto;
        height: 280px;
        display: flex;
        justify-content: flex-start;
        flex-wrap: wrap;
    }
    .answer_sheet .bk-button {
        margin-left: 10px;
        margin-top: 20px;
    }
    .answer_sheet hr {
        width: 90%;
    }
    .answer_sheet_explain{
        height: auto;
    }
    .answer_explain_button{
        display: block;
        margin-left: 25%;
    }
    .answer_explain_button .bk-button{
        margin: 0 auto;
    }
    .progress {
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .bk-progress {
        width: 60%;
        margin-right: 20px;
        display: inline-block;
    }
    .answer {
        height: 400px;
        border: 1px solid #888888;
        border-radius: 7px;
    }
    .answer h3 {
        text-align: center;
    }
    .last {
        position: absolute;
        top: 35%;
    }
    .next {
        position: absolute;
        right: 0px;
        top: 35%;
    }
    .question_box {
        height: 280px;
        width: 80%;
        overflow: hidden;
        position: relative;
        margin: 0 auto;
    }
    .answer ul {
        min-height: 100000px;
        width: 600px;
        position: absolute;
        top: 0;
        left: 0;
    }
    .answer ul li {
        height: 280px;
        width: 100%;
        /*border: 1px solid green !important;*/
        margin: 0 auto;
        overflow: auto;
    }
    .answer_submit hr {
        position: relative;
        width: 90%;
    }
    .answer_submit_button {
        display: block;
        margin-left: 45%;
    }
</style>
