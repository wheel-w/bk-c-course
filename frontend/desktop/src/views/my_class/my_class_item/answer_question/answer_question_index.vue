<template>
    <div class="wrapper">
        我是答题首页（展示当前课程所有的试题）
        <bk-button theme="primary" @click="startAnswer.primary.visible = true">
            开始答题
        </bk-button>
        <bk-dialog v-model="startAnswer.primary.visible" :confirm-fn="toDetail"
            theme="primary"
            :mask-close="false"
            :header-position="startAnswer.primary.headerPosition"
            title="开始答题">
            是否确认开始答题？
        </bk-dialog>
    </div>
</template>

<script>
    import { bkButton, bkDialog } from 'bk-magic-vue'
    export default {
        name: 'answer_question_index',
        components: {
            bkButton,
            bkDialog
        },
        data () {
            return {
                startAnswer: {
                    primary: {
                        visible: false,
                        headerPosition: 'left'
                    }
                }
            }
        },
        methods: {
            toDetail () {
                this.$router.push({
                    name: 'answer_question_detail'
                })
            }
        }
        
    }
</script>

<style scoped>
    
</style>
