<template>
    <div>
        <bk-form :model="Question" :label-width="0" ref="Question">
            <div class="question">
                <p>题目:</p>
                <bk-form-item :required="true" :rules="rules.question" :property="'question'" error-display-type="normal">
                    <bk-input
                        type="textarea"
                        :autosize="{ minRows: 2, maxRows: 2 }"
                        placeholder="请输入题目内容"
                        v-model="Question.question"
                        style="width:84%;">
                    </bk-input>
                </bk-form-item>
            </div>
            <div class="options">
                <bk-form-item :required="true" :rules="rules.answer" :property="'answer'" error-display-type="normal">
                    <bk-radio-group v-model="Question.answer">
                        <div class="option" @click="chooseT">
                            <bk-radio name="T" value="true" style="margin-top: 38px;margin-left:10px;">
                                T
                            </bk-radio>
                        </div>
                        <div class="option" @click="chooseF">
                            <bk-radio name="F" value="false" style="margin-top: 38px;margin-left:10px;">
                                F
                            </bk-radio>
                        </div>
                    </bk-radio-group>
                </bk-form-item>
            </div>
            <div class="rightAnswer">
                <p>正确答案：{{Question.answer}}</p>
            </div>
            <div class="analysis">
                <bk-switcher
                    theme="primary"
                    v-model="explainOpen"
                    :show-text="true"
                    on-text="解析"
                    off-text="解析"
                    @change="handleSwitcherChange">
                </bk-switcher>
                <bk-button class="reset" theme="primary" @click="reset">重置</bk-button>
                <bk-button class="upload" theme="primary" @click="checkData">上传</bk-button>
                <bk-form-item :required="true" :rules="rules.explain" :property="'explain'" v-if="explainOpen" error-display-type="normal">
                    <bk-input
                        type="textarea"
                        :autosize="{ minRows: 2, maxRows: 2 }"
                        placeholder="请输入答案解析内容"
                        v-model="Question.explain"
                        v-if="explainOpen"
                        style="width:84%;display:block;margin-top:10px">
                    </bk-input>
                </bk-form-item>
            </div>
        </bk-form>
    </div>
</template>
<script>
    export default {
        name: 'QuestionRadio',
        props: {
            info: {
                type: Object,
                default: {
                    question: null,
                    explain: null,
                    answer: null,
                    types: '判断题'
                }
            },
            editable: {
                type: Boolean,
                default: false
            }
        },
        data () {
            return {
                config: {
                    message: null,
                    theme: 'error',
                    offset: 80
                },
                explainOpen: false,
                Question: JSON.parse(JSON.stringify(this.info)),
                rules: {
                    question: [
                        {
                            required: true,
                            message: '题目内容不能为空！',
                            trigger: 'blur'
                        }
                    ],
                    option: [
                        {
                            required: true,
                            message: '选项内容不能为空！',
                            trigger: 'blur'
                        }
                    ],
                    answer: [
                        {
                            required: true,
                            message: '答案不能为空',
                            trigger: 'blur'
                        }
                    ],
                    explain: [
                        {
                            required: true,
                            message: '答案解析不能为空！',
                            trigger: 'blur'
                        }
                    ]
                }
            }
        },
        created () {
            if (this.editable) {
                if (this.Question.explain) {
                    this.explainOpen = true
                }
            }
        },
        methods: {
            chooseT () {
                this.Question.answer = 'true'
            },
            chooseF () {
                this.Question.answer = 'false'
            },
            handleSwitcherChange (status) {
                if (!status) {
                    this.Question.analysis = null
                }
            },
            checkData () {
                this.$refs.Question.validate().then(validator => {
                    if (this.editable) {
                        this.$emit('updateQuestion', this.Question)
                    } else {
                        this.$emit('createQuestion', this.Question)
                    }
                }, validator => {
                    this.config.message = validator.content
                    this.config.theme = 'error'
                    this.$bkMessage(this.config)
                })
            },
            reset () {
                this.Question.question = null
                this.Question.option_A = null
                this.Question.option_B = null
                this.Question.option_C = null
                this.Question.option_D = null
                this.Question.option_E = null
                this.Question.answer = null
                this.Question.explain = null
                this.explainOpen = false
                this.$refs.Question.clearError()
            }
        }
    }
</script>
<style lang="postcss" scoped>
.question {
    height: 110px;
    margin-left: 1%;
    p {
        width:80%;
    }
}
.options {
    height: 140px;
    margin-left: 1%;
    margin-top: 10px;
    .option {
        border-width: 1px;
        border-radius: 5px;
        border-color: #1768EF;
        border-style: solid;
        height:100px;
        width: 39%;
        margin-right: 6%;
        margin-bottom: 10px;
        display: inline-block;
    }
}
.rightAnswer {
    margin-left: 1%;
}
.analysis {
    height: 125px;
    margin-left: 1%;
    .reset {
        margin-left: 66.6%;
    }
}
</style>
