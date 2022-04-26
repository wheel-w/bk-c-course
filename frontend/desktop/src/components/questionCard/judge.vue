<template>
    <div class="judge">
        <bk-card title="判断题">
            <bk-form form-type="inline" model="judgeData">
                <bk-form-item>
                    <bk-input behavior="simplicity" :clearable="true" v-model="judgeData.title" placeholder="请输入标题"
                        style="width: 300px"></bk-input>
                </bk-form-item>
                <bk-form-item>
                    <bk-input behavior="simplicity" :clearable="true" v-model="judgeData.describe" placeholder="添加描述：文字、图片或链接"
                        style="width: 300px"></bk-input>
                </bk-form-item>
                <bk-form-item>
                    <bk-radio-group v-model="judgeData.options">
                        <bk-radio :value="'T'">
                            <bk-input behavior="simplicity" :clearable="true" v-model="judgeData.options.A" placeholder="正确答案"
                                style="width: 250px"></bk-input>
                        </bk-radio>
                        <bk-radio :value="'F'">
                            <bk-input behavior="simplicity" :clearable="true" v-model="judgeData.options.B" placeholder="错误答案"
                                style="width: 250px"></bk-input>
                        </bk-radio>
                    </bk-radio-group>
                </bk-form-item>
                <bk-form-item>
                    <bk-button theme="default" size="small" title="提交" icon="check-1" class="mr10">确定</bk-button>
                    <bk-button theme="default" size="small" title="新增" icon="plus" class="mr10">新增</bk-button>
                    <bk-button theme="default" size="small" title="删除" icon="close" class="mr10">删除</bk-button>
                </bk-form-item>
            </bk-form>
        </bk-card>
    </div>
</template>

<script>
    export default {
        name: 'judge',
        components: 'judge',
        data () {
            return {
                judgeData: {
                    title: '',
                    describe: '',
                    options: {
                        'T': '',
                        'F': ''
                    }
                }
            }
        }
    }
</script>

<style scoped>
    .judge{
        width: 400px;
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
