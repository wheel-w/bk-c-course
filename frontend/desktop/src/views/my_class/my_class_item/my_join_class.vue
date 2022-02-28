<template>
    <div class="wrapper">
        我是课程管理主界面
        <bk-button :theme="'primary'" @click="toDetail">
            点击进入课程详情页面
        </bk-button>
    </div>
</template>

<script>
    export default {
        name: 'my_join_class',
        methods: {
            toDetail () {
                this.$router.push({
                    name: 'my_join_class_detail'
                })
            }
        }
    }
</script>

<style scoped>

</style>
