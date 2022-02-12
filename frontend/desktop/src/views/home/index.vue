<template>
    <div class="wrapper">
        <div class="header">
            <h2>我的课程</h2>
            <bk-button theme="primary" @click="toMyClass">
                新增课程
            </bk-button>
        </div>
        <div class="content">
            <div class="content-item" v-for="item in courseList" :key="item.course_id" @click="toMyClassDetail(item.course_id)">
                <h3 style="margin: 0; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">{{ item.course_name }}</h3>
                <span>课程id：{{ item.course_id }}</span>
                <span>任教老师：{{ item.teacher }}</span>
            </div>
        </div>
    </div>
</template>

<script>
    import { bus } from '@/common/bus'

    export default {
        name: 'index',
        data () {
            return {
                // 课程列表
                courseList: []
            }
        },
        created () {
            this.getCourseList()
        },
        methods: {
            // 跳转至课程管理界面
            toMyClass () {
                bus.$emit('updateNavId', 'my_join_class')
                this.$router.replace({
                    name: 'my_join_class'
                })
            },
            // 跳转至点击的课程详情页面
            toMyClassDetail (id) {
                bus.$emit('updateNavId', 'my_join_class')
                this.$store.commit('updateCourseId', id)
                this.$router.replace({
                    name: 'my_join_class_detail'
                })
            },
            // 获取课程列表
            async getCourseList () {
                this.$http.get('/course/find_courses/').then(res => {
                    if (res.data.length !== 0) {
                        this.courseList = res.data
                    }
                })
            }
        }
    }
</script>

<style scoped>
.wrapper {
    display: flex;
    flex-direction: column;
    height: 580px;
}

.header {
    width: 20%;
    display: flex;
    align-items: center;
    justify-content: space-around;
}

.content {
    display: flex;
    flex-wrap: wrap;
    overflow-y: auto;
}
.content-item {
    width: 20%;
    margin: 10px 2.5%;
    height: 100px;
    border-radius: 3px;
    background-image: linear-gradient(to right, #f0f1f5, #e4e5e9);
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    padding-left: 1%;
}
.content-item:hover {
    cursor: pointer;
    transition: 300ms;
    box-shadow: 0 5px 8px 0 rgba(0, 0, 0, 0.19);
}
</style>
