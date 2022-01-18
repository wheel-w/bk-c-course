<template>
    <div class="wrapper">
        我是答题页面（暂时放在子nav中，后期应通过点击事件跳转到此页面）
        <bk-button theme="primary" @click="test">
            接口测试
        </bk-button>
        {{res}}
    </div>
</template>

<script>
    export default {
        name: 'answer_question',
        data () {
            return {
                res: {}
            }
        },
        methods: {
            async test () {
                this.$http.get('/course/find_courses/').then(res => {
                    this.res = res
                })
            }
        }
    }
</script>

<style scoped>

</style>
