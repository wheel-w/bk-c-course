<template>
    <div class="wrapper">
        我是出题首页（展示当前课程所有出的卷子）
        <bk-button :theme="'primary'" @click="toDetail">
            点击进入出题详情页面
        </bk-button>
    </div>
</template>

<script>
    export default {
        name: 'set_question_index',
        methods: {
            toDetail () {
                this.$router.push({
                    name: 'set_question_detail'
                })
            }
        }
    }
</script>

<style scoped>

</style>
