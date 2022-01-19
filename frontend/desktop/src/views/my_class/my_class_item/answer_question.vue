<template>
    <div class="wrapper">
        <div class="header">
            <div class="header-left-card">

            </div>
            <div class="header-right-card">

            </div>
        </div>
        <bk-button theme="primary" @click="test">
            接口测试
        </bk-button>
        {{ res }}
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
                // this.$http.get('/course/find_courses/').then(res => {
                //     this.res = res
                // })
                this.$http.post('/course/manage_course/', {
                    course_name: '高等数学',
                    teacher: '王文成',
                    course_introduction: '高等数学是一个非常好的学科',
                    manage_student: '白郑鑫'
                }).then(res => {
                    this.res = res
                })
            }
        }
    }
</script>

<style scoped>
.header {
  padding: 5px 15px 15px 15px;
  font-size: 14px;
  color: #737987;
  height: 84px;
  background: #FFFFFF;
  -webkit-box-shadow: 0px 2px 4px 0px rgb(25 25 41 / 5%);
  box-shadow: 0px 2px 4px 0px rgb(25 25 41 / 5%);
  border-radius: 2px;
  border: 1px solid rgba(220,222,229,1);
}
</style>
