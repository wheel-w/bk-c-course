export default {
    props: {
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
                        message: '题目内容不能为空',
                        trigger: 'change'
                    }
                ],
                option: [
                    {
                        required: true,
                        message: '选项内容不能为空',
                        trigger: 'change'
                    }
                ],
                answer: [
                    {
                        required: true,
                        message: '答案不能为空',
                        trigger: 'change'
                    }
                ],
                explain: [
                    {
                        required: true,
                        message: '答案解析不能为空',
                        trigger: 'change'
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
        checkData () {
            console.log('mixin-checkdata')
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
        handleSwitcherChange (status) {
            if (!status && !this.readonly) {
                this.Question.explain = null
            }
        }
    }
}
