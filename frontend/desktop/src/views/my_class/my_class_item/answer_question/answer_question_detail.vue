<template>
    <div class="myWrapper" v-if="$route.query.isAccomplish" ref="top">
        <div class="header">
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
                    <div style="margin-top: 10px">
                        正确答案为：
                        <span v-if="childItem.types === 'JUDGE'">{{ item.answer === 'false' ? 'F' : 'T' }}</span>
                        <span v-else>{{ childItem.answer }}</span>
                    </div>
                    <div style="margin-top: 10px">
                        解析：<span>{{ childItem.explain === null ? '暂无解析' : childItem.explain}}</span>
                    </div>
                    <div style="margin-top: 10px">
                        得分：{{ childItem.student_score }}
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
            <ul id="answer_sheet_title">
                <li v-for="(value, key) in questionTitle" :key="key">
                    <strong v-if="key !== 'cumulative_time'">{{key}}</strong>
                    <ul id="answer_sheet_number" v-if="key !== 'cumulative_time'">
                        <li v-for="item in questionTitle[key]" :key="item.id">
                            <bk-button v-if="(item.student_answer === '') || (item.student_answer === null) || (item.student_answer === '[]')" :theme="'primary'" type="submit" class="mr10 switchQuestion" size="small" @click="selectQuestion(item.id)">{{item.id}}</bk-button>
                            <bk-button v-else-if="(item.student_answer !== '') && (item.student_answer !== null) && (item.student_answer !== '[]')" :theme="'success'" type="submit" class="mr10 switchQuestion" size="small" @click="selectQuestion(item.id)">{{item.id}}</bk-button>
                        </li>
                    </ul><br>
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
                        <li class="question_item" v-for="item in questionList" :key="item.id">{{item.id}}.{{item.question}}
                            <div v-if="item.types === 'SINGLE'">
                                <bk-radio-group v-model="item.student_answer">
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
                                <p class="mb5">我的答案：{{item.student_answer}}</p>
                            </div>
                            <div v-else-if="item.types === 'MULTIPLE'">
                                <bk-checkbox-group v-model="item.student_answer">
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
                                <p class="mb5">我的答案：{{item.student_answer}}</p>
                            </div>
                            <div v-else-if="item.types === 'JUDGE'">
                                <bk-radio-group v-model="item.student_answer">
                                    <bk-radio :value="'T'">
                                        T. 正确
                                    </bk-radio>
                                    <br>
                                    <bk-radio :value="'F'">
                                        F. 错误
                                    </bk-radio>
                                    <br>
                                </bk-radio-group>
                                <p class="mb5">我的答案：{{item.student_answer}}</p>
                            </div>
                            <div v-else-if="item.types === 'COMPLETION'">
                                <div class="input-answer">
                                    <bk-input placeholder="请输入你的答案" :type="'textarea'" :rows="3" :maxlength="255"
                                        v-model="item.student_answer">
                                    </bk-input>
                                </div>
                                <p class="mb5">我的答案：{{item.student_answer}}</p>
                            </div>
                            <div v-else-if="item.types === 'SHORT_ANSWER'">
                                <div class="input-answer">
                                    <bk-input placeholder="请输入你的答案" :type="'textarea'" :rows="3" :maxlength="255"
                                        v-model="item.student_answer">
                                    </bk-input>
                                </div>
                                <p class="mb5">我的答案：{{item.student_answer}}</p>
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
                questionList: [],
                questionTitle: {},
                answer_info: [],
                paper_id: 0
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
            if (this.$route.query.isAccomplish) {
                this.getStudentQuestionList()
            } else {
                this.Time() // 调用定时器
                this.getPaperStatus() // 调用获取题目接口
                const that = this
                setTimeout(function () {
                    that.submitButtonDisabled()
                }, 2000)
            }
        },
        methods: {
            // 获取问题列表
            async getStudentQuestionList () {
                this.$http.get('/course/answer_or_check_paper/', { params: { paper_id: this.paper_id } }).then(res => {
                    this.totalQuestion = res.data
                    this.totalScore = res.data.total_score
                    delete this.totalQuestion['total_score']
                    delete this.totalQuestion['cumulative_time']
                    for (const item in this.totalQuestion) {
                        for (const childItem of this.totalQuestion[item]) {
                            if (childItem.student_answer === null) {
                                childItem.student_answer = '未作答'
                            }
                        }
                    }
                })
            },
            // 时 分 秒 格式化函数
            countDown () {
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
                    this.countDown()
                    this.submitButtonDisabled()
                }, 1000)
            },
            clickSavaAnswer () {
                this.$bkInfo({
                    title: '确认要保存当前作答？',
                    confirmLoading: true,
                    confirmFn: async () => {
                        try {
                            await new Promise(resolve => {
                                setTimeout(() => {
                                    resolve('成功')
                                }, 1500)
                            })
                            this.saveAnswer()
                            return true
                        } catch (e) {
                            console.warn(e)
                            return false
                        }
                    }
                })
            },
            saveAnswer () {
                this.questionList.forEach(e => {
                    this.answer_info.push({ question_id: e.id, stu_answers: e.student_answer
                    })
                })
                console.log('answer_info', this.answer_info)
                this.$http.post('course/save_answer/', { paper_id: this.paper_id, answer_info: this.answer_info, save_or_submit: 1, cumulative_time: this.seconds }).then(res => {
                    console.log(res)
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
                this.$bkInfo({
                    title: '确认要提交当前试卷？',
                    confirmLoading: true,
                    confirmFn: async () => {
                        try {
                            await new Promise(resolve => {
                                setTimeout(() => {
                                    resolve('成功')
                                }, 1500)
                            })
                            this.submitAnswer()
                            this.toAnswerQuestionIndex()
                            return true
                        } catch (e) {
                            console.warn(e)
                            return false
                        }
                    }
                })
            },
            submitAnswer () {
                this.questionList.forEach(e => {
                    this.answer_info.push({ question_id: e.id, stu_answers: e.student_answer
                    })
                })
                console.log('answer_info', this.answer_info)
                this.$http.post('course/save_answer/', { paper_id: this.paper_id, answer_info: this.answer_info, save_or_submit: 0, cumulative_time: this.seconds }).then(res => {
                    console.log(res)
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
                this.$router.push({
                    name: 'answer_question_index'
                })
            },
            lastQuestion () {
                const ul = document.querySelector('.question_lists')
                const li = document.querySelectorAll('.question_item')
                const lilength = li.length
                const liheight = li[0].offsetHeight
                const relativeheight = lilength * liheight
                ul.style.width = relativeheight + 'px'
                let ultop = ul.offsetTop
                if (-(ultop) > 0 && ultop < relativeheight * 4) {
                    ultop = ultop + liheight
                    ul.style.top = ultop + 'px'
                }
            },
            nextQuestion () {
                const ul = document.querySelector('.question_lists')
                const li = document.querySelectorAll('.question_item')
                const lilength = li.length
                const liheight = li[0].offsetHeight
                const relativeheight = lilength * liheight
                ul.style.height = lilength * liheight + 'px'
                let ultop = ul.offsetTop
                if (-(ultop) < relativeheight - 280) {
                    ultop = ultop - liheight
                    ul.style.top = ultop + 'px'
                }
            },
            selectQuestion (num) {
                const ul = document.querySelector('.question_lists')
                const li = document.querySelectorAll('.question_item')
                let currentnum = this.questionList[0].id
                const liheight = li[0].offsetHeight
                let ultop = ul.offsetTop
                ultop = (currentnum - num) * liheight
                ul.style.top = ultop + 'px'
                currentnum = num
            },
            getPaperStatus () {
                this.$http.get('/course/get_paper_status/', { params: { paper_id: this.paper_id } }).then(res => {
                    console.log('paper_status', res)
                    if (res.data.paper_status === 'RELEASE' || res.data.paper_status === 'DRAFT') {
                        this.getQuestionList()
                    } else if (res.data.paper_status !== 'RELEASE') {
                        this.$bkMessage({
                            message: res.message,
                            theme: 'error'
                        })
                        this.toAnswerQuestionIndex()
                    }
                })
            },
            getQuestionList () {
                this.$http.get('/course/answer_or_check_paper/', { params: { paper_id: this.paper_id } }).then(res => {
                    this.questionTitle = res.data
                    console.log('questList', res.data)
                    this.seconds = res.data.cumulative_time
                    for (const key in res.data) {
                        // 答题卡id排序
                        res.data[key].sort(function (a, b) {
                            return a.question_id - b.question_id
                        })
                        for (const item in res.data[key]) {
                            this.questionList.push(res.data[key][item])
                        }
                    }
                    // 题目id排序
                    this.questionList.sort(function (a, b) {
                        return a.question_id - b.question_id
                    })
                })
            },
            submitButtonDisabled () {
                // 判断是否存在没有做完的题目
                const someResult = this.questionList.some(function (item) {
                    return item.student_answer === '' || item.student_answer === null || item.student_answer === '[]'
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
    #answer_sheet_title{
        margin-left: 20px;
        height: 280px;
        overflow: auto;
    }
    #answer_sheet_number{
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
