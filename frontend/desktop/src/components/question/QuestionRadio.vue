<template>
    <div>
        <bk-form :model="Question" :label-width="0" ref="Question">
            <div class="question">
                <p>题目:</p>
                <bk-form-item :required="true" :rules="rules.question" :property="'question'" error-display-type="normal">
                    <bk-input
                        type="textarea"
                        :readonly="readonly"
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
                        <div class="optionAC">
                            <bk-form-item :required="true" :rules="rules.option" :property="'option_A'" :icon-offset="50" error-display-type="tooltips">
                                <bk-radio name="A" value="A" :disabled="readonly">
                                    <bk-input ref="optionA" v-model="Question.option_A" :readonly="readonly" placeholder="请输入选项A内容" size="large" style="width:400px;">
                                        <template slot="prepend">
                                            <div class="group-text">A</div>
                                        </template>
                                    </bk-input>
                                </bk-radio>
                            </bk-form-item>
                        </div>
                        <div class="optionBD">
                            <bk-form-item :required="true" :rules="rules.option" :property="'option_B'" :icon-offset="50">
                                <bk-radio name="B" value="B" :disabled="readonly">
                                    <bk-input ref="optionB" v-model="Question.option_B" :readonly="readonly" placeholder="请输入选项B内容" size="large" style="width:400px;" @enter="nextOption('C')">
                                        <template slot="prepend">
                                            <div class="group-text">B</div>
                                        </template>
                                    </bk-input>
                                </bk-radio>
                            </bk-form-item>
                        </div>
                        <div class="optionAC">
                            <bk-form-item :required="true" :rules="rules.option" :property="'option_C'" :icon-offset="50">
                                <bk-radio name="C" value="C" :disabled="readonly">
                                    <bk-input ref="optionC" v-model="Question.option_C" :readonly="readonly" placeholder="请输入选项C内容" size="large" style="width:400px;" @enter="nextOption('D')">
                                        <template slot="prepend">
                                            <div class="group-text">C</div>
                                        </template>
                                    </bk-input>
                                </bk-radio>
                            </bk-form-item>
                        </div>
                        <div class="optionBD">
                            <bk-form-item :required="true" :rules="rules.option" :property="'option_D'" :icon-offset="50">
                                <bk-radio name="D" value="D" :disabled="readonly">
                                    <bk-input ref="optionD" v-model="Question.option_D" :readonly="readonly" placeholder="请输入选项D内容" size="large" style="width:400px;" @enter="nextOption('A')">
                                        <template slot="prepend">
                                            <div class="group-text">D</div>
                                        </template>
                                    </bk-input>
                                </bk-radio>
                            </bk-form-item>
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
                <bk-button v-if="!readonly" class="reset" theme="primary" @click="reset">重置</bk-button>
                <bk-button v-if="!readonly" class="upload" theme="primary" @click="checkData">上传</bk-button>
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
            <div class="upload">
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
                    option_A: null,
                    option_B: null,
                    option_C: null,
                    option_D: null,
                    explain: null,
                    answer: null,
                    types: '单选题'
                }
            },
            editable: {
                type: Boolean,
                default: false
            },
            readonly: {
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
                Question: JSON.parse(JSON.stringify(this.info)),
                explainOpen: false,
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
                            message: '答案不能为空！',
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
            if (this.Question.explain) {
                this.explainOpen = true
            }
        },
        methods: {
            handleSwitcherChange (status) {
                if (!status && !this.readonly) {
                    this.Question.explain = null
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
            },
            nextOption (option) {
                if (option === 'A') {
                    this.$refs.optionA.focus()
                } else if (option === 'B') {
                    this.$refs.optionB.focus()
                } else if (option === 'C') {
                    this.$refs.optionC.focus()
                } else {
                    this.$refs.optionD.focus()
                }
            }
        }
    }
</script>
<style lang="postcss" scoped>
.question {
    height: 110px;
    padding-left: 1%;
    p {
        width:80%;
    }
}
.options {
    height: 140px;
    margin-left: 1%;
    margin-top: 10px;
    .optionAC {
        width: 40%;
        margin-right: 7%;
        margin-bottom: 10px;
        display: inline-block;
    }
    .optionBD {
        width: 40%;
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
