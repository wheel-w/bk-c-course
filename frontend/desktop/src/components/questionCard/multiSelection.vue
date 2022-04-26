<template>
    <div class="multiSelection">
        <bk-card title="多选题">
            <bk-form form-type="inline" model="multiSelectData">
                <bk-form-item>
                    <bk-input behavior="simplicity" :clearable="true" v-model="multiSelectData.title" placeholder="请输入标题"
                        style="width: 300px"></bk-input>
                </bk-form-item>
                <bk-form-item>
                    <bk-input behavior="simplicity" :clearable="true" v-model="multiSelectData.describe" placeholder="添加描述：文字、图片或链接"
                        style="width: 300px"></bk-input>
                </bk-form-item>
                <bk-form-item>
                    <bk-checkbox-group v-model="multiSelectData.options">
                        <bk-checkbox :value="'A'">
                            <bk-input behavior="simplicity" :clearable="true" v-model="multiSelectData.options.A" placeholder="选项一"
                                style="width: 250px"></bk-input>
                        </bk-checkbox>
                        <bk-checkbox :value="'B'">
                            <bk-input behavior="simplicity" :clearable="true" v-model="multiSelectData.options.B" placeholder="选项二"
                                style="width: 250px"></bk-input>
                        </bk-checkbox>
                        <bk-checkbox :value="'C'">
                            <bk-input behavior="simplicity" :clearable="true" v-model="multiSelectData.options.C" placeholder="选项三"
                                style="width: 250px"></bk-input>
                        </bk-checkbox>
                        <bk-checkbox :value="'D'">
                            <bk-input behavior="simplicity" :clearable="true" v-model="multiSelectData.options.D" placeholder="选项四"
                                style="width: 250px"></bk-input>
                        </bk-checkbox>
                    </bk-checkbox-group>
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
        name: 'multiSelection',
        components: 'multiSelection',
        data () {
            return {
                multiSelectData: {
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
    .multiSelection{
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
