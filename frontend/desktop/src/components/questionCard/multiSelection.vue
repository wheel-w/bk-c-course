<template>
    <div class="multiSelection">
        <bk-card title="多选题">
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
                    <bk-checkbox-group>
                        <bk-checkbox :value="'A'">
                            <span>A：</span>
                            <bk-input behavior="simplicity" :clearable="true" v-model="questionData.option_A" placeholder="选项一"
                                style="width: 300px"></bk-input>
                        </bk-checkbox>
                        <bk-checkbox :value="'B'">
                            <span>B：</span>
                            <bk-input behavior="simplicity" :clearable="true" v-model="questionData.option_B" placeholder="选项二"
                                style="width: 300px"></bk-input>
                        </bk-checkbox>
                        <bk-checkbox :value="'C'">
                            <span>C：</span>
                            <bk-input behavior="simplicity" :clearable="true" v-model="questionData.option_C" placeholder="选项三"
                                style="width: 300px"></bk-input>
                        </bk-checkbox>
                        <bk-checkbox :value="'D'">
                            <span>D：</span>
                            <bk-input behavior="simplicity" :clearable="true" v-model="questionData.option_D" placeholder="选项四"
                                style="width: 300px"></bk-input>
                        </bk-checkbox>
                        <bk-checkbox :value="'E'">
                            <span>E：</span>
                            <bk-input behavior="simplicity" :clearable="true" v-model="questionData.option_E" placeholder="选项五"
                                style="width: 300px"></bk-input>
                        </bk-checkbox>
                    </bk-checkbox-group>
                </bk-form-item>
                <bk-form-item>
                    <bk-input behavior="simplicity" :clearable="true" v-model="questionData.answer" placeholder="请输入正确答案"
                        style="width: 350px"></bk-input>
                </bk-form-item>
                <bk-form-item>
                    <bk-input behavior="simplicity" :clearable="true" v-model="questionData.explain" placeholder="请输入题目解析"
                        style="width: 350px"></bk-input>
                </bk-form-item>
                <bk-form-item>
                    <bk-button theme="default" size="small" title="提交" icon="check-1" @click="conf" class="mr10" :disabled="confirmStatus">添加该题目</bk-button>
                    <bk-button theme="default" size="small" title="新增" icon="plus" @click="add" class="mr10">新增</bk-button>
                    <bk-button theme="default" size="small" title="删除" icon="close" @click="del" class="mr10">删除</bk-button>
                </bk-form-item>
            </bk-form>
        </bk-card>
    </div>
</template>

<script>
    export default {
        name: 'multiSelection',
        components: 'multiSelection',
        data () {
            return {
                questionData: {
                    types: 'MULTIPLE',
                    title: '',
                    question_url: '',
                    option_A: '',
                    option_B: '',
                    option_C: '',
                    option_D: '',
                    option_E: '',
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
    .multiSelection{
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
