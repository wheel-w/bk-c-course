<template>
    <div class="body">
        <div class="upload">
            <bk-upload
                :tip="'只允许上传.xls的文件'"
                :with-credentials="true"
                :custom-request="addExcel"
                :handle-res-code="true"
                :limit="1"
                :accept="'.xls'"
                style="width:100%;"
            ></bk-upload>
        </div>
        <a href="http://dev.paas-edu.bktencent.com:8000/course/download_set_question_excel_template/">下载模板</a>
    </div>
</template>
<script>
    export default {
        name: 'QuestionImport',
        props: {
            chapterid: {
                type: Number,
                default: null
            }
        },
        data () {
            return {
                config: {
                    message: null,
                    theme: 'error',
                    offset: 80
                }
            }
        },
        methods: {
            downloadSetQuestionExcelTemplate () {
                window.open('http://dev.paas-edu.bktencent.com:8000/course/download_set_question_excel_template/')
            },
            testSuccess (file, fileList) {
                console.log(file, fileList, 'success')
            },
            testProgress (e, file, fileList) {
                this.update(e)
            },
            testDone () {
            },
            testErr (file, fileList) {
            },
            handleRes (response) {
                if (response.id) {
                    return true
                }
                return false
            },
            addExcel (param) {
                if (this.chapterid) {
                    const data = new FormData()
                    data.append('excel_file', param.fileList[0].origin)
                    data.append('course_id', this.$store.state.currentCourseId)
                    data.append('chapter_id', this.chapterid)
                    const config = {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    }
                    this.$http.post('/course/import_question_excel/', data, config).then(res => {
                        this.config.theme = 'success'
                        this.config.message = res.message
                        this.$bkMessage(this.config)
                    })
                } else {
                    this.config.theme = 'error'
                    this.config.message = '章节不能为空！'
                    this.$bkMessage(this.config)
                }
            }
        }
    }
</script>
<style lang="postcss" scoped>
.body {
    .upload {
        width: 100%;
        height: 105px;
        overflow: hidden;
    }
}
</style>
