<template>
    <div class="wrapper">
        这是首页
        {{ res }}
        <bk-button theme="primary" @click="primary.visible = true">
            新建课程
        </bk-button>
        <bk-dialog v-model="primary.visible" @confirm="createCourse"
            theme="primary"
            :mask-close="false"
            title="新增课程">
            <span>课程名称：</span>
            <bk-input v-model="uploadCourse.course_name"></bk-input>
            <span>授课老师：</span>
            <bk-input v-model="uploadCourse.teacher"></bk-input>
            <span>课程简介：</span>
            <bk-input v-model="uploadCourse.course_introduction"></bk-input>
            <span>学生管理员：</span>
            <bk-input v-model="uploadCourse.manage_student"></bk-input>
        </bk-dialog>
    </div>
</template>

<script>
    export default {
        name: 'index',
        data () {
            return {
                // 对话框控制属性
                primary: {
                    visible: false,
                    headerPosition: 'left'
                },
                // 上传的课程信息
                uploadCourse: {
                    course_name: '',
                    teacher: '',
                    course_introduction: '',
                    manage_student: ''
                },
                // 网络请求返回响应数据
                res: {}
            }
        },
        methods: {
            async createCourse () {
                this.$http.post('/course/manage_course/', this.uploadCourse).then(res => {
                    this.res = res
                })
            }
        }
    }
</script>
