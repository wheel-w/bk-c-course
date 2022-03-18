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
                    <bk-checkbox-group v-model="Question.answer">
                        <div class="wrapper">
                            <bk-container :col="12" :gutter="4">
                                <bk-row>
                                    <bk-col :span="6">
                                        <div :class="optionStyle('A')" @dblclick="handleOptionDbclick('A')" @mouseover="mouseOver = 'A'" @mouseleave="mouseOver = ''">
                                            <bk-form-item :required="true" :rules="rules.option" :property="'option_A'" error-display-type="tooltips">
                                                <bk-checkbox v-if="option !== 'A'" :value="'A'" style="margin-top:10px;margin-left:10px;display:inline-block;">
                                                    <p>{{'A.' + Question.option_A}}</p>
                                                </bk-checkbox>
                                                <bk-input v-else ref="optionA" behavior="simplicity" v-model="Question.option_A" :readonly="readonly" placeholder="请输入选项A内容" size="large" @blur="option = ''" @enter="option = ''" style="width:100%;margin-bottom:6px">
                                                </bk-input>
                                            </bk-form-item>
                                        </div>
                                    </bk-col>
                                    <bk-col :span="6">
                                        <div :class="optionStyle('B')" @dblclick="handleOptionDbclick('B')" @mouseover="mouseOver = 'B'" @mouseleave="mouseOver = ''">
                                            <bk-form-item :required="true" :rules="rules.option" :property="'option_B'" error-display-type="tooltips">
                                                <bk-checkbox v-if="option !== 'B'" :value="'B'" style="margin-top:10px;margin-left:10px;display:inline-block;">
                                                    <p>{{'B.' + Question.option_B}}</p>
                                                </bk-checkbox>
                                                <bk-input v-else ref="optionB" behavior="simplicity" v-model="Question.option_B" :readonly="readonly" placeholder="请输入选项B内容" size="large" @blur="option = ''" @enter="option = ''" style="width:100%;margin-bottom:6px">
                                                </bk-input>
                                            </bk-form-item>
                                        </div>
                                    </bk-col>
                                </bk-row>
                                <bk-row>
                                    <bk-col :span="6">
                                        <div :class="optionStyle('C')" @dblclick="handleOptionDbclick('C')" @mouseover="mouseOver = 'C'" @mouseleave="mouseOver = ''">
                                            <bk-form-item :required="true" :rules="rules.option" :property="'option_C'" error-display-type="tooltips">
                                                <bk-checkbox v-if="option !== 'C'" :value="'C'" style="margin-top:10px;margin-left:10px;display:inline-block;">
                                                    <p>{{'C.' + Question.option_C}}</p>
                                                </bk-checkbox>
                                                <bk-input v-else ref="optionC" behavior="simplicity" v-model="Question.option_C" :readonly="readonly" placeholder="请输入选项C内容" size="large" @blur="option = ''" @enter="option = ''" style="width:100%;margin-bottom:6px">
                                                </bk-input>
                                            </bk-form-item>
                                        </div>
                                    </bk-col>
                                    <bk-col :span="6">
                                        <div :class="optionStyle('D')" @dblclick="handleOptionDbclick('D')" @mouseover="mouseOver = 'D'" @mouseleave="mouseOver = ''">
                                            <bk-form-item :required="true" :rules="rules.option" :property="'option_D'" error-display-type="tooltips">
                                                <bk-checkbox v-if="option !== 'D'" :value="'D'" style="margin-top:10px;margin-left:10px;display:inline-block;">
                                                    <p>{{'D.' + Question.option_D}}</p>
                                                </bk-checkbox>
                                                <bk-input v-else ref="optionD" behavior="simplicity" v-model="Question.option_D" :readonly="readonly" placeholder="请输入选项D内容" size="large" @blur="option = ''" @enter="option = ''" style="width:100%;margin-bottom:6px">
                                                </bk-input>
                                            </bk-form-item>
                                        </div>
                                    </bk-col>
                                </bk-row>
                                <bk-row>
                                    <bk-col :span="6">
                                        <div :class="optionStyle('E')" @dblclick="handleOptionDbclick('E')" @mouseover="mouseOver = 'E'" @mouseleave="mouseOver = ''">
                                            <bk-form-item :required="true" :rules="rules.option" :property="'option_E'" error-display-type="tooltips">
                                                <bk-checkbox v-if="option !== 'E'" :value="'E'" style="margin-top:10px;margin-left:10px;display:inline-block;">
                                                    <p>{{'E.' + Question.option_E}}</p>
                                                </bk-checkbox>
                                                <bk-input v-if="option === 'E'" ref="optionE" behavior="simplicity" v-model="Question.option_E" :readonly="readonly" placeholder="请输入选项C内容" size="large" @blur="option = ''" @enter="option = ''" style="width:100%;margin-bottom:6px">
                                                </bk-input>
                                            </bk-form-item>
                                        </div>
                                    </bk-col>
                                    <bk-col :span="6">
                                    </bk-col>
                                </bk-row>
                            </bk-container>
                        </div>
                    </bk-checkbox-group>
                </bk-form-item>
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
                        style="width:100%;display:block;margin-top:5px">
                    </bk-input>
                </bk-form-item>
            </div>
        </bk-form>
    </div>
</template>
<script>
    import questionMixin from '@/mixin/questionMixin.js'
    export default {
        name: 'QuestionRadio',
        mixins: [questionMixin],
        props: {
            info: {
                type: Object,
                default: {
                    question: null,
                    option_A: '',
                    option_B: '',
                    option_C: '',
                    option_D: '',
                    option_E: '',
                    explain: null,
                    answer: [],
                    types: '多选题'
                }
            }
        },
        data () {
            return {
                option: ''
            }
        },
        computed: {
            optionStyle () {
                return (option) => {
                    if (option === 'A' || option === 'C' || option === 'E') {
                        if (this.Question.answer.indexOf(option) >= 0) {
                            return 'choosed optionAC'
                        } else if (this.mouseOver === option) {
                            return 'mouseOver-style optionAC'
                        } else {
                            return 'not-choosed optionAC'
                        }
                    } else {
                        if (this.Question.answer.indexOf(option) >= 0) {
                            return 'choosed optionBD'
                        } else if (this.mouseOver === option) {
                            return 'mouseOver-style optionBD'
                        } else {
                            return 'not-choosed optionBD'
                        }
                    }
                }
            }
        },
        watch: {
        },
        created () {
            if (this.editable) {
                this.Question.answer = this.Question.answer.split('')
            }
        },
        methods: {
            handleOptionDbclick (option) {
                this.option = option
                this.$nextTick(() => {
                    if (option === 'A') {
                        this.$refs.optionA.focus()
                    } else if (option === 'B') {
                        this.$refs.optionB.focus()
                    } else if (option === 'C') {
                        this.$refs.optionC.focus()
                    } else if (option === 'D') {
                        this.$refs.optionD.focus()
                    } else {
                        this.$refs.optionE.focus()
                    }
                })
            },
            checkData () {
                this.$refs.Question.validate().then(validator => {
                    this.Question.answer = this.Question.answer.join('')
                    if (this.editable) {
                        this.$emit('updateQuestion', this.Question)
                    } else {
                        this.$emit('createQuestion', this.Question)
                    }
                    this.Question.answer = this.Question.answer.split('')
                }, validator => {
                    this.config.message = validator.content
                    this.config.theme = 'error'
                    this.$bkMessage(this.config)
                })
            },
            reset () {
                this.Question.question = null
                this.Question.option_A = ''
                this.Question.option_B = ''
                this.Question.option_C = ''
                this.Question.option_D = ''
                this.Question.option_E = ''
                this.Question.answer = []
                this.Question.explain = null
                this.explainOpen = false
                this.$refs.Question.clearError()
            }
        }
    }
</script>
<style lang="postcss" scoped>
.bk-form-radio .bk-radio-text {
    width: 80%;
}
.wrapper {
    overflow: hidden;
    border: 1px solid #ddd;
    border-radius: 2px;
    padding: 10px 0;
    height: 165px;
}
.mouseOver-style {
    border-style: solid;
    border-width: 2px;
    border-radius: 15px;
    border-color: #3A84FF;
}
.choosed {
    border-style: solid;
    border-width: 2px;
    border-radius: 15px;
    border-color: #3A84FF;
    background-color: #E1ECFF;
}
.not-choosed {
    border-style: solid;
    border-width: 2px;
    border-radius: 15px;
    border-color: #C4C6CC;
}
.question {
    height: 110px;
    margin-left: 1%;
    p {
        width:80%;
    }
}
.options {
    height: 199px;
    width: 84%;
    padding-left: 1%;
    .optionAC {
        width: 90%;
        height: 43px;
        margin-bottom: 10px;
        padding: 0px 10px;
        display: inline-block;
        p{
            width: 200px;
            overflow:hidden;
            text-overflow:ellipsis;
            -o-text-overflow:ellipsis;
            white-space:nowrap;
        }
    }
    .optionBD {
        width: 90%;
        float: right;
        height: 43px;
        margin-bottom: 10px;
        padding: 0px 10px;
        display: inline-block;
        box-sizing: border-box;
        /* background-color: #E1ECFF; */
        p{
            width: 200px;
            overflow:hidden;
            text-overflow:ellipsis;
            -o-text-overflow:ellipsis;
            white-space:nowrap;
        }
    }
}
.rightAnswer {
    margin-left: 1%;
}
.analysis {
    width: 83%;
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
