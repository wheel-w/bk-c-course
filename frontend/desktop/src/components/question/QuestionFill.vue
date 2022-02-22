<template>
    <div class="question-fill">
        <bk-form :model="Question" :label-width="0" ref="Question">
            <div class="question">
                <p>题目:</p>
                <div class="question1">
                    <bk-form-item :required="true" :rules="rules.question" :property="'question'" error-display-type="normal">
                        <bk-input
                            type="textarea"
                            :autosize="{ minRows: 4, maxRows: 4 }"
                            placeholder="请输入题目内容"
                            v-model="Question.question"
                            style="width:84%;"
                            @focus="handleInputFocus"
                            @change="handleInputChange"
                            @mouseup="handleMouseSelect">
                        </bk-input>
                    </bk-form-item>
                </div>
                <p>用鼠标选中下列文本的内容进行挖空:</p>
                <bk-form-item :required="true" :rules="rules.answer" :property="'answer'" error-display-type="normal">
                    <div class="hollow">
                        <label @mouseup="handleMouseSelect" style="display: block;">{{Question.question}}</label>
                    </div>
                </bk-form-item>
            </div>
            <div class="rightAnswer">
                <p style="display:inline-block;">正确答案:</p>
                <bk-tag
                    theme="info"
                    :key="tag"
                    v-for="(tag,index) in answer"
                    closable
                    :disable-transitions="false"
                    @close="handleClose(tag)"
                    style="display:inline-block;">
                    {{'填空' + (index + 1) + ':' + tag.text}}
                </bk-tag>
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
        name: 'QuestionFill',
        props: {
            info: {
                type: Object,
                default: {
                    question: null,
                    explain: null,
                    answer: [],
                    types: '填空题'
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
                separator: ' ',
                explainOpen: false,
                answer: [],
                Question: JSON.parse(JSON.stringify(this.info)),
                rules: {
                    question: [
                        {
                            required: true,
                            message: '题目内容不能为空！',
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
        },
        created () {
            if (this.editable) {
                this.exchange()
                if (this.Question.explain) {
                    this.explainOpen = true
                }
            }
        },
        methods: {
            exchange () {
                const answer1 = this.Question.answer.split(this.separator)
                const question = this.Question.question.split('')
                for (let i = 0; i < question.length - 6; i++) {
                    if (question.slice(i, i + 7).join('') === '_______') {
                        const text = answer1.shift()
                        this.answer.push({
                            text: text,
                            start: i,
                            length: text.length
                        })
                        i = i + 6
                    }
                }
            },
            checkData () {
                if (this.editable) {
                    this.Question.answer = []
                }
                this.answer.forEach(element => {
                    this.Question.answer.push(element.text)
                })
                this.Question.answer = this.Question.answer.join(this.separator)
                this.$refs.Question.validate().then(validator => {
                    if (this.editable) {
                        this.$emit('updateQuestion', this.Question)
                    } else {
                        this.$emit('createQuestion', this.Question)
                    }
                    this.Question.answer = this.Question.answer.split(this.separator)
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
                this.answer = []
                this.Question.explain = null
                this.explainOpen = false
                this.$refs.Question.clearError()
            },
            handleMouseSelect () {
                console.log(111)
                const text = window.getSelection().toString()
                const start = window.getSelection().anchorOffset
                // const end = window.getSelection().focusOffset
                if (text && text.indexOf('_') < 0) {
                    this.answer.push({
                        text: text,
                        start: start,
                        length: text.length
                    })
                    this.ascending_sort(this.answer, 'start')
                    this.answer.forEach(element => {
                        if (element.start > start) {
                            element.start = element.start + 7 - text.length
                        }
                    })
                    const question = this.Question.question.split('')
                    question.splice(start, text.length, '_______')
                    // for (let i = start; i < end; i++) {
                    //     question[i] = '_'
                    // }
                    this.Question.question = question.join('')
                }
            },
            handleClose (tag) {
                const question = this.Question.question.split('')
                question.splice(tag.start, 7, tag.text)
                this.answer.forEach(element => {
                    if (element.start > tag.start) {
                        element.start = element.start + tag.length - 7
                        element.end = element.end + tag.length - 7
                    }
                })
                // for (let i = tag.start; i < tag.end; i++) {
                //     question[i] = text[i - tag.start]
                // }
                this.Question.question = question.join('') // 对删除的填空的内容进行恢复
                this.answer.splice(this.answer.indexOf(tag), 1) // 删除填空
            },
            ascending_sort (array, key) {
                return array.sort(function (a, b) {
                    const x = a[key]
                    const y = b[key]
                    return ((x < y) ? -1 : (x > y) ? 1 : 0)
                })
            },
            handleSwitcherChange (status) {
                if (!status) {
                    this.Question.analysis = null
                }
            },
            handleInputChange (value, event) {
            },
            handleInputFocus (value, event) {
            }
        }
    }
</script>
<style lang="postcss" scoped>
.question {
    height: 230px;
    margin-left:1%;
    .question1 {
        height: 90px;
    }
    p {
        width:80%;
    }
    .hollow::-webkit-scrollbar {
        display: none;
    }
    .hollow {
        border-style: solid;
        border-width: 1px;
        border-radius: 5px;
        border-color: #1768EF;
        width: 84%;
        height: 80px;
        overflow: scroll;
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
