<template>
    <div class="wrapper">
        我是课程详情页面，当前课程id为{{ $store.state.currentCourseId }}
    </div>
</template>

<script>
    export default {
        name: 'my_join_class_detail',
        data () {
            return {}
        },
        watch: {
            // 监听当前课程id的变化
            '$store.state.currentCourseId' (newValue) {
                // 发送网络请求更新课程信息
                console.log(newValue)
            }
        }
    }
</script>

<style scoped>

</style>
