<template>
    <div>
        <bk-form :model="Question" :label-width="0" ref="Question">
            <div class="question">
                <p>题目:</p>
                <bk-form-item :required="true" :rules="rules.question" :property="'question'" error-display-type="normal">
                    <bk-input
                        type="textarea"
                        :autosize="{ minRows: 4, maxRows: 4 }"
                        :readonly="readonly"
                        placeholder="请输入题目内容"
                        v-model="Question.question"
                        style="width:84%;">
                    </bk-input>
                </bk-form-item>
            </div>
            <div class="rightAnswer">
                <p>正确答案:</p>
                <bk-form-item :required="true" :rules="rules.answer" :property="'answer'" error-display-type="normal">
                    <bk-input
                        type="textarea"
                        :autosize="{ minRows: 4, maxRows: 4 }"
                        :readonly="readonly"
                        placeholder="请输入正确答案内容"
                        v-model="Question.answer"
                        style="width:84%;">
                    </bk-input>
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
    import questionMixin from '@/mixin/questionMixin.js'
    export default {
        name: 'QuestionShort',
        mixins: [questionMixin],
        props: {
            info: {
                type: Object,
                default: {
                    question: null,
                    answer: null,
                    explain: null,
                    types: '简答题'
                }
            }
        },
        data () {
            return {
            }
        },
        created () {
        },
        methods: {
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
.radioQuestion {
    margin-left: %;
}
.question {
    height: 110px;
    padding-left: 1%;
    p {
        width:80%;
    }
}
.rightAnswer {
    height: 140px;
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
