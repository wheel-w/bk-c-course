<template>
    <div class="wrapper" v-if="$route.query.isAccomplish">
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
                你的答案：<span>{{ item.student_answer }}</span>
            </div>
            <div style="margin-top: 10px">
                正确答案为：<span>{{ item.answer }}</span>
            </div>
            <div style="margin-top: 10px">
                解析：<span>{{ item.explain === null ? '暂无解析' : item.explain}}</span>
            </div>
            <div style="margin-top: 10px">
                得分：{{ item.student_score }}
            </div>
        </bk-card>

        <h3>二、填空题</h3>
        <bk-card class="radio-common" :title="`${index + 1}.${item.question} （${item.score}分）`" v-for="(item,index) in summaryQuestionList" :key="index" :border="false">
            <div>
                你的答案：<span>{{ item.student_answer }}</span>
            </div>
            <div style="margin-top: 10px">
                正确答案为：
                <span v-if="item.types === 'JUDGE'">{{ item.answer === 'false' ? 'F' : 'T' }}</span>
                <span v-else>{{ item.answer }}</span>
            </div>
            <div style="margin-top: 10px">
                解析：<span>{{ item.explain === null ? '暂无解析' : item.explain}}</span>
            </div>
            <div style="margin-top: 10px">
                得分：{{ item.student_score }}
            </div>
        </bk-card>

        <h3>三、主观题</h3>
        <bk-card class="radio-common" :title="`${index + 1}.${item.question} （${item.score}分）`" v-for="(item,index) in shortQuestionList" :key="index" :border="false">
            <div>
                你的答案：<span>{{ item.student_answer }}</span>
            </div>
            <div style="margin-top: 10px">
                正确答案为：<span>{{ item.answer }}</span>
            </div>
            <div style="margin-top: 10px">
                解析：<span>{{ item.explain === null ? '暂无解析' : item.explain}}</span>
            </div>
            <div style="margin-top: 10px">
                得分：{{ item.student_score }}
            </div>
        </bk-card>
    </div>
    <div class="wrapper" v-else>
        这是答题详细界面
    </div>
</template>

<script>
    export default {
        name: 'answer_question_detail',
        data () {
            return {
                choiceQuestionList: [],
                summaryQuestionList: [],
                shortQuestionList: []
            }
        },
        mounted () {
            this.getQuestionList()
        },
        methods: {
            // 获取问题列表
            async getQuestionList () {
                this.$http.get('/course/mark_or_check_paper/', { params: { paper_id: 6, student_id: 4 } }).then(res => {
                    this.choiceQuestionList = res.data.选择题
                    this.summaryQuestionList = res.data.填空题
                    this.shortQuestionList = res.data.名词解释
                    console.log(res.data)
                })
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

</style>
