<template>
    <div class="singleSelection">
        <bk-card title="单选题">
            <bk-form form-type="inline" model="singleData">
                <bk-form-item>
                    <bk-input behavior="simplicity" :clearable="true" v-model="singleData.title" placeholder="请输入标题"
                        style="width: 300px"></bk-input>
                </bk-form-item>
                <bk-form-item>
                    <bk-input behavior="simplicity" :clearable="true" v-model="singleData.describe" placeholder="添加描述：文字、图片或链接"
                        style="width: 300px"></bk-input>
                </bk-form-item>
                <bk-form-item>
                    <bk-radio-group v-model="singleData.options">
                        <bk-radio :value="'A'">
                            <bk-input behavior="simplicity" :clearable="true" v-model="singleData.options.A" placeholder="选项一"
                                style="width: 250px"></bk-input>
                        </bk-radio>
                        <bk-radio :value="'B'">
                            <bk-input behavior="simplicity" :clearable="true" v-model="singleData.options.B" placeholder="选项二"
                                style="width: 250px"></bk-input>
                        </bk-radio>
                        <bk-radio :value="'C'">
                            <bk-input behavior="simplicity" :clearable="true" v-model="singleData.options.C" placeholder="选项三"
                                style="width: 250px"></bk-input>
                        </bk-radio>
                        <bk-radio :value="'D'">
                            <bk-input behavior="simplicity" :clearable="true" v-model="singleData.options.D" placeholder="选项四"
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
        name: 'singleSelection',
        components: 'singleSelection',
        data () {
            return {
                singleData: {
                    title: '',
                    describe: '',
                    options: {
                        'A': '',
                        'B': '',
                        'C': '',
                        'D': ''
                    }
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
        /*border-radius: 10px !important;*/
        background-color: #ffffff;
        border: 0px solid #ffffff;
        /*border: 1px solid #bbde4f;*/
    }
    .bk-form-item .bk-button{
        margin-top: 20px;
    }
</style>
