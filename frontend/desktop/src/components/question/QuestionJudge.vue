<template>
    <div>
        <bk-form :model="Question" :label-width="0" ref="Question">
            <div class="question">
                <p>题目:</p>
                <bk-form-item :required="true" :rules="rules.question" :property="'question'" error-display-type="normal">
                    <bk-input
                        type="textarea"
                        :autosize="{ minRows: 2, maxRows: 2 }"
                        :readonly="readonly"
                        placeholder="请输入题目内容"
                        v-model="Question.question"
                        style="width:84%;">
                    </bk-input>
                </bk-form-item>
            </div>
            <div class="options" v-if="!readonly">
                <bk-form-item :required="true" :rules="rules.answer" :property="'answer'" error-display-type="normal">
                    <bk-radio-group v-model="Question.answer">
                        <div :class="optionStyle('true')" @click="choose('true')" @mouseover="mouseOver = 'true'" @mouseleave="mouseOver = ''">
                            <bk-radio name="T" value="true" style="margin-top: 38px;margin-left:10px;">
                                正确
                            </bk-radio>
                        </div>
                        <div :class="optionStyle('false')" @click="choose('false')" @mouseover="mouseOver = 'false'" @mouseleave="mouseOver = ''">
                            <bk-radio name="F" value="false" style="margin-top: 38px;margin-left:10px;">
                                错误
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
                <bk-button v-if="!readonly" class="reset" theme="primary" @click="reset">重置</bk-button>
                <bk-button v-if="!readonly" class="upload" theme="primary" @click="checkData">上传</bk-button>
                <bk-form-item :required="true" :rules="rules.explain" :property="'explain'" v-if="explainOpen" error-display-type="normal">
                    <bk-input
                        type="textarea"
                        :autosize="{ minRows: 2, maxRows: 2 }"
                        :readonly="readonly"
                        placeholder="请输入答案解析内容"
                        v-model="Question.explain"
                        v-if="explainOpen"
                        style="width:100%;display:block;margin-top:10px">
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
        computed: {
            optionStyle () {
                return (option) => {
                    if (this.Question.answer === option) {
                        return 'choosed-style'
                    } else if (this.mouseOver === option) {
                        return 'mouseover-style'
                    } else {
                        return 'option'
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
                this.Question.answer = option
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
                this.Question.answer = null
                this.Question.explain = null
                this.explainOpen = false
                this.$refs.Question.clearError()
            }
        }
    }
</script>
<style lang="postcss" scoped>
.mouseover-style {
    border-width: 2px;
    border-radius: 5px;
    border-color: #979BA5;
    border-style: solid;
    background-color: #EAEBF0;
    height:100px;
    width: 39%;
    margin-right: 6%;
    margin-bottom: 10px;
    display: inline-block;
}
.choosed-style {
    border-width: 2px;
    border-radius: 5px;
    border-color: #3A84FF;
    border-style: solid;
    background-color: #E1ECFF;
    height:100px;
    width: 39%;
    margin-right: 6%;
    margin-bottom: 10px;
    display: inline-block;
}
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
        border-color: #979BA5;
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
