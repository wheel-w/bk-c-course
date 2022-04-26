<template>
    <div class="singleSelection">
        <div class="shortAnswer">
            <bk-card title="简答题">
                <bk-form form-type="inline" model="shortAnswerData">
                    <bk-form-item>
                        <bk-input behavior="simplicity" :clearable="true" v-model="shortAnswerData.title" placeholder="请输入标题"
                            style="width: 300px"></bk-input>
                    </bk-form-item>
                    <bk-form-item>
                        <bk-input behavior="simplicity" :clearable="true" v-model="shortAnswerData.describe" placeholder="添加描述：文字、图片或链接"
                            style="width: 300px"></bk-input>
                    </bk-form-item>
                    <bk-form-item>
                        <bk-input
                            placeholder="请输入该问题答案"
                            :type="'textarea'"
                            :rows="3"
                            :maxlength="255" style="width: 300px; margin-top:10px"
                            v-model="shortAnswerData.answer">
                        </bk-input>
                    </bk-form-item>
                    <bk-form-item>
                        <bk-button theme="default" size="small" title="提交" icon="check-1" class="mr10">确定</bk-button>
                        <bk-button theme="default" size="small" title="新增" icon="plus" class="mr10">新增</bk-button>
                        <bk-button theme="default" size="small" title="删除" icon="close" class="mr10">删除</bk-button>
                    </bk-form-item>
                </bk-form>
            </bk-card>

        </div>
    </div>
</template>

<script>
    export default {
        name: 'singleSelection',
        components: 'singleSelection',
        data () {
            return {
                shortAnswerData: {
                    title: '',
                    describe: ''
                }
            }
        }
    }
</script>

<style scoped>
    .singleSelection{
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
