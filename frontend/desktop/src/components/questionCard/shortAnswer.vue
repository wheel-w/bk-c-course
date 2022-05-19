<template>
    <div class="shortAnswer">
        <div class="shortAnswer">
            <bk-card title="简答题">
                <bk-form form-type="inline" model="questionData">
                    <bk-form-item>
                        <bk-input behavior="simplicity" :clearable="true" v-model="questionData.title" placeholder="请输入标题"
                            style="width: 450px"></bk-input>
                    </bk-form-item>
                    <bk-form-item>
                        <span>分数：</span>
                        <bk-input behavior="simplicity" :clearable="true" v-model="questionData.score" placeholder="请设置分数"
                            style="width: 200px"></bk-input>
                    </bk-form-item>
                    <bk-form-item>
                        <bk-input
                            placeholder="请输入正确答案"
                            :type="'textarea'"
                            :rows="3"
                            :maxlength="255" style="width: 350px; margin-top:10px"
                            v-model="questionData.answer">
                        </bk-input>
                    </bk-form-item>
                    <bk-form-item>
                        <bk-input
                            placeholder="请输入该题解析"
                            :type="'textarea'"
                            :rows="3"
                            :maxlength="255" style="width: 350px; margin-top:10px"
                            v-model="questionData.explain">
                        </bk-input>
                    </bk-form-item>
                    <bk-form-item>
                        <bk-button theme="default" size="small" title="提交" icon="check-1" @click="conf" class="mr10" :disabled="confirmStatus">添加该题目</bk-button>
                        <bk-button theme="default" size="small" title="新增" icon="plus" @click="add" class="mr10">新增</bk-button>
                        <bk-button theme="default" size="small" title="删除" icon="close" @click="del" class="mr10">删除</bk-button>
                    </bk-form-item>
                </bk-form>
            </bk-card>

        </div>
    </div>
</template>

<script>
    export default {
        name: 'shortAnswer',
        components: 'shortAnswer',
        data () {
            return {
                questionData: {
                    types: 'SHORT_ANSWER',
                    title: '',
                    question_url: '',
                    answer: '',
                    answer_url: '',
                    explain: '',
                    explain_url: '',
                    score: ''
                },
                confirmStatus: false
            }
        },
        methods: {
            add () {
                this.$emit('add')
            },
            del () {
                // 子组件向父组件传值（此处传递一个空值） - 父组件将执行getContent方法
                this.$emit('func', '')
            },
            conf () {
                if (this.questionData.title === '' || this.questionData.title === null) {
                    this.$bkMessage({
                        message: '标题不能为空，请输入标题！',
                        theme: 'warning'
                    })
                } else if (this.questionData.answer === '' || this.questionData.answer === null) {
                    this.$bkMessage({
                        message: '正确答案不能为空, 请输入正确答案！',
                        theme: 'warning'
                    })
                } else {
                    this.$emit('confirms', { questionData: this.questionData })
                    this.confirmStatus = true
                    this.$bkMessage({
                        message: '该题目添加成功！',
                        theme: 'primary'
                    })
                }
            }
        }
    }
</script>

<style scoped>
    .shortAnswer{
        width: 98%;
        display: block;
        margin-top: 1%;
        margin-bottom: 1%;
    }
    .bk-card{
       background-color: #ffffff;
        border: 0px solid #ffffff;
    }
    .bk-form-item .bk-button{
        margin-top: 20px;
    }
</style>
