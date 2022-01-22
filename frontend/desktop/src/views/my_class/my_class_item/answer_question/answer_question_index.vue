<template>
    <div class="wrapper">
        我是答题首页（展示当前课程所有的试题）
        <bk-button :theme="'primary'" @click="toDetail">
            点击进入答题详情页面
        </bk-button>
    </div>
</template>

<script>
    export default {
        name: 'answer_question_index',
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
