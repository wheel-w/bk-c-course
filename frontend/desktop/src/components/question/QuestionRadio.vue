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
                        style="width:100%;">
                    </bk-input>
                </bk-form-item>
            </div>
            <div class="options">
                <bk-form-item :required="true" :rules="rules.answer" :property="'answer'" error-display-type="normal">
                    <bk-radio-group v-model="Question.answer">
                        <div :class="optionStyle('A')">
                            <bk-form-item :required="true" :rules="rules.option" :property="'option_A'" :icon-offset="20" error-display-type="tooltips">
                                <bk-input ref="optionA" v-model="Question.option_A" :readonly="readonly" placeholder="请输入选项A内容" size="large" style="width:100%;">
                                    <template slot="prepend">
                                        <div class="group-text" @click="choose('A')" @mouseover="mouseOver = 'A'" @mouseleave="mouseOver = ''"><label>A</label></div>
                                    </template>
                                </bk-input>
                            </bk-form-item>
                        </div>
                        <div :class="optionStyle('B')">
                            <bk-form-item :required="true" :rules="rules.option" :property="'option_B'" :icon-offset="20">
                                <bk-input ref="optionB" v-model="Question.option_B" :readonly="readonly" placeholder="请输入选项B内容" size="large" style="width:100%;" @enter="nextOption('C')">
                                    <template slot="prepend">
                                        <div class="group-text" @click="choose('B')" @mouseover="mouseOver = 'B'" @mouseleave="mouseOver = ''"><label>B</label></div>
                                    </template>
                                </bk-input>
                            </bk-form-item>
                        </div>
                        <div :class="optionStyle('C')">
                            <bk-form-item :required="true" :rules="rules.option" :property="'option_C'" :icon-offset="20">
                                <bk-input ref="optionC" v-model="Question.option_C" :readonly="readonly" placeholder="请输入选项C内容" size="large" style="width:100%;" @enter="nextOption('D')">
                                    <template slot="prepend">
                                        <div class="group-text" @click="choose('C')" @mouseover="mouseOver = 'C'" @mouseleave="mouseOver = ''"><label>C</label></div>
                                    </template>
                                </bk-input>
                            </bk-form-item>
                        </div>
                        <div :class="optionStyle('D')">
                            <bk-form-item :required="true" :rules="rules.option" :property="'option_D'" :icon-offset="20">
                                <bk-input ref="optionD" v-model="Question.option_D" :readonly="readonly" placeholder="请输入选项D内容" size="large" style="width:100%;" @enter="nextOption('A')">
                                    <template slot="prepend">
                                        <div class="group-text" @click="choose('D')" @mouseover="mouseOver = 'D'" @mouseleave="mouseOver = ''"><label>D</label></div>
                                    </template>
                                </bk-input>
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
                        style="width:100%;display:block;margin-top:10px">
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
                mouseOver: '',
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
                            trigger: 'change'
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
        computed: {
            optionStyle () {
                return (option) => {
                    if (option === 'A' || option === 'C') {
                        if (this.Question.answer === option) {
                            return 'optionAC choosed-style'
                        } else if (this.mouseOver === option) {
                            return 'optionAC mouseOver-style'
                        } else {
                            return 'optionAC'
                        }
                    } else {
                        if (this.Question.answer === option) {
                            return 'optionBD choosed-style'
                        } else if (this.mouseOver === option) {
                            return 'optionBD mouseOver-style'
                        } else {
                            return 'optionBD'
                        }
                    }
                }
            }
        },
        created () {
            if (this.Question.explain) {
                this.explainOpen = true
            }
        },
        methods: {
            choose (option) {
                if (!this.readonly) {
                    this.Question.answer = option
                }
            },
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
.mouseOver-style {
    background-color: #C4C6CC;
}
.choosed-style {
    background-color: #1768EF;
}
.question {
    width: 84%;
    height: 110px;
    padding-left: 1%;
    p {
        width:80%;
    }
}
.options {
    height: 150px;
    width: 84%;
    padding-left: 1%;
    .optionAC {
        width: 45%;
        border-radius: 2px;
        margin-right: 10%;
        margin-bottom: 10px;
        padding: 3px 3px 3px 3px;
        display: inline-block;
        box-sizing: border-box;
    }
    .optionBD {
        width: 45%;
        border-radius: 2px;
        margin-bottom: 10px;
        padding: 3px 3px 3px 3px;
        display: inline-block;
        box-sizing: border-box;
    }
}
.rightAnswer {
    margin-left: 1%;
}
.analysis {
    width: 84%;
    height: 125px;
    margin-left: 1%;
    .upload {
        float: right;
    }
    .reset {
        margin-left: 10px;
        float: right;
    }
}
</style>
