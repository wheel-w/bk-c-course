<template>
    <div class="wrapper">
        <div class="header">
            <h2>我的项目</h2>
            <bk-button theme="primary" @click="toMyClass" style="margin-left: 2vw">
                <!--<bk-button v-if="$store.state.user.identity === 'TEACHER'" theme="primary" @click="toMyClass" style="margin-left: 2vw">-->
                新增课程
            </bk-button>
        </div>
        <div class="content">
            <div class="content-item" v-for="item in courseList" :key="item.id">
                <h3 style="margin: 0; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">{{ item.name }}</h3>
                <p>项目id：{{ item.id }}</p>
                <p>创建人：{{ item.creator }}</p>
                <a href="#" @click="toMyClassDetail(item.course_id)"><span>查看项目任务</span></a>
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
                bus.$emit('updateNavId', 'mycourse')
                this.$router.replace({
                    name: 'my_course'
                })
            },
            // 跳转至点击的课程详情页面
            toMyClassDetail (id) {
                bus.$emit('updateNavId', 'answer_question_index')
                this.$store.commit('updateCourseId', id)
                this.$router.replace({
                    name: 'answer_question_index'
                })
            },
            // 获取课程列表
            async getCourseList () {
                this.$http.get('/api/project/').then(res => {
                    console.log('res------')
                    if (res.data.count !== 0) {
                        this.courseList = res.data.results
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
        width: 20vw;
        display: flex;
        align-items: center;
        justify-content: flex-start;
    }
    .bk-button.bk-primary {
        background: #88a2ef;
        border-color: #88a2ef;
        color: #fff;
    }
    .content {
        display: flex;
        flex-wrap: wrap;
        overflow-y: auto;
    }
    .content-item {
        /*width: 300px;*/
        margin: 20px;
        padding: 20px 40px;
        background: #ebf5fc;
        border-radius: 10px;
        box-shadow: -6px -6px 20px rgba(255, 255, 255, 1),
    }
    .content-item:hover {
        transition: 300ms;
        box-shadow: inset -6px -6px 10px rgba(255, 255, 255, 0.5), inset 6px 6px 20px rgba(0, 0, 0, 0.05);
    }
    .content-item a{
        display: inline-block;
        padding: 10px 20px;
        margin-top: 15px;
        border-radius: 10px;
        color: #32a3b1;
        font-size: 16px;
        text-decoration: none;
        box-shadow: -4px -4px 15px rgba(255, 255, 255, 1), 4px 4px 15px rgba(0, 0, 0, .1);
    }
    .content-item a:hover{
        box-shadow: inset -4px -4px 10px rgba(255, 255, 255, 0.5), inset 4px 4px 10px rgba(0, 0, 0, .1);
    }
    .content-item a:hover span{
        display: block;
        transform: scale(0.98);
    }
    .content-item h3{
        color: #32a3b1;
        font-weight: 700;
        font-size: 1.4em;
        letter-spacing: 2px;
    }
    .content-item p{
        color: #32a3b1;
    }
</style>
