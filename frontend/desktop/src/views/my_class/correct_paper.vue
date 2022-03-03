<template>
    <div class="wrapper">
        <h2>试卷信息</h2>
        <div class="studentInfo">
            <span>学生班级：物网191</span>
            <span>学生姓名：白郑鑫</span>
            <span>学生学号：3190932002</span>
        </div>
        <h3>一、选择题</h3>
        <bk-card class="radio-common" :title="`${index + 1}.${item.question} （${item.score}分）`" v-for="(item,index) in choiceQuestionList" :key="index" :border="false">
            <bk-radio-group v-if="item.types === 'SINGLE'" class="radio-common" v-model="item.student_answer">
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
            <bk-checkbox-group v-if="item.types === 'MULTIPLE'" class="radio-common" v-model="item.student_answer">
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
            <bk-divider></bk-divider>
            <div style="margin-top: 10px">
                学生答案：<span>{{ item.student_answer }}</span>
            </div>
            <div style="margin-top: 10px">
                正确答案为：<span>{{ item.answer }}</span>
            </div>
            <div style="margin-top: 10px">
                打分：<bk-input type="number" style="width: 110px" v-model="item.student_score" :max="item.score" :min="0"></bk-input>
            </div>
        </bk-card>

        <h3>二、填空题</h3>
        <bk-card class="radio-common" :title="`${index + 1}.${item.question} （${item.score}分）`" v-for="(item,index) in summaryQuestionList" :key="index" :border="false">
            <div>
                学生答案：<span>{{ item.student_answer }}</span>
            </div>
            <div style="margin-top: 10px">
                正确答案为：
                <span v-if="item.types === 'JUDGE'">{{ item.answer === 'false' ? 'F' : 'T' }}</span>
                <span v-else>{{ item.answer }}</span>
            </div>
            <div style="margin-top: 10px">
                打分：<bk-input type="number" style="width: 110px" v-model="item.student_score" :max="item.score" :min="0"></bk-input>
            </div>
        </bk-card>

        <h3>三、主观题</h3>
        <bk-card class="radio-common" :title="`${index + 1}.${item.question} （${item.score}分）`" v-for="(item,index) in shortQuestionList" :key="index" :border="false">
            <div>
                学生答案：<span>{{ item.student_answer }}</span>
            </div>
            <div style="margin-top: 10px">
                正确答案为：<span>{{ item.answer }}</span>
            </div>
            <div style="margin-top: 10px">
                打分：<bk-input type="number" style="width: 110px" v-model="item.student_score" :max="item.score" :min="0"></bk-input>
            </div>
        </bk-card>

        <bk-button style="width: 120px;position: fixed; bottom: 120px; right: 6%;" :theme="'primary'" type="submit" @click="checkAnswer">确认批改</bk-button>

    </div>
</template>

<script>
    export default {
        name: 'correct_paper',
        data () {
            return {
                choiceQuestionList: [],
                summaryQuestionList: [],
                shortQuestionList: [],
                uploadData: {
                    student_answer_list: [],
                    paper_id: 6
                }
            }
        },
        mounted () {
            this.getQuestionList()
        },
        methods: {
            // 获取题目列表
            async getQuestionList () {
                this.$http.get('/course/mark_or_check_paper/', { params: { paper_id: 6, student_id: 4 } }).then(res => {
                    this.choiceQuestionList = res.data.选择题
                    this.summaryQuestionList = res.data.填空题
                    this.shortQuestionList = res.data.名词解释
                    console.log(res.data)
                })
            },
            // 发起批改试卷请求
            async checkAnswer () {
                this.uploadData = {
                    student_answer_list: [],
                    paper_id: 6
                }
                for (const value of this.choiceQuestionList) {
                    this.uploadData.student_answer_list.push(
                        {
                            id: value.student_answer_id,
                            score: value.student_score
                        }
                    )
                }
                for (const value of this.summaryQuestionList) {
                    this.uploadData.student_answer_list.push(
                        {
                            id: value.student_answer_id,
                            score: value.student_score
                        }
                    )
                }
                for (const value of this.shortQuestionList) {
                    this.uploadData.student_answer_list.push(
                        {
                            id: value.student_answer_id,
                            score: value.student_score
                        }
                    )
                }
                console.log(this.uploadData)
                // this.$http.post('/course/teacher_correct_paper/', this.uploadData).then(res => {
                //     console.log(res)
                // })
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
</style>
