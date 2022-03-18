<template>
    <div class="create_question">
        <div>
            <bk-select :disabled="false" v-model="curChapterId" style="width: 25%;display:inline-block;"
                ext-cls="select-custom"
                ext-popover-cls="select-popover-custom"
                searchable
                placeholder="请选择章节"
                @selected="handleSelected"
                @change="handleChapterChange"
                @clear="handleChapterClear">
                <bk-option v-for="chapter in chapterList"
                    :key="chapter.id"
                    :id="chapter.id"
                    :name="chapter.chapter_name">
                </bk-option>
            </bk-select>
            <chapter-manage :key="componentKey1" :chapters="chapterList" :chapterid="curChapterId" @updateChapter="updateChapter"></chapter-manage>
        </div>
        <div class="set_question" style="border-style:;height:480px;margin-bottom:30px;">
            <bk-tab :active.sync="active" type="border-card" label-height="50" :active-bar="activeBar2" @tab-change="handleTabChange">
                <bk-tab-panel
                    v-for="(panel, index) in panels"
                    v-bind="panel"
                    :key="index"
                    style="height:420px;">
                    <keep-alive :key="componentKey2">
                        <component :is="active" :chapterid="curChapterId" @createQuestion="createQuestion" @importQuestionExcel="getQuestionList()"></component>
                    </keep-alive>
                </bk-tab-panel>
            </bk-tab>
        </div>
        <bk-dialog v-model="editQuestion.visable" width="1200" :draggable="false" :show-footer="false">
            <component v-if="editQuestion.visable" :is="Dict[editQuestion.Question.types]" :info="editQuestion.Question" :editable="true" @updateQuestion="updateQuestion"></component>
        </bk-dialog>
        <div class="questions">
            <bk-button theme="primary" :outline="true" @click="deleteQuestions" style="margin-bottom: 10px">批量删除</bk-button>
            <bk-table
                :data="showQuestionList1"
                :size="size"
                :outer-border="true"
                :virtual-render="true"
                :key="componentKey"
                :pagination="pagination"
                :highlight-current-row="true"
                @filter-change="handleFilterChange"
                @selection-change="handleSelectChange"
                @page-change="handlePageChange"
                @page-limit-change="handlePageLimitChange"
                @row-click="handleRowClick"
                height="500">
                <bk-table-column type="selection" :width="60" v-model="selection"></bk-table-column>
                <bk-table-column
                    label="题目id"
                    prop="question_id"
                    width="200">
                </bk-table-column>
                <bk-table-column
                    label="题目内容"
                    prop="question">
                </bk-table-column>
                <bk-table-column
                    label="题目类型"
                    prop="types"
                    width="200"
                    :filtered-value="curType"
                    :filters="[{ text: '单选题', value: 'SINGLE' }, { text: '多选题', value: 'MULTIPLE' }, { text: '判断题', value: 'JUDGE' }, { text: '填空题', value: 'COMPLETION' }, { text: '简答题', value: 'SHORT_ANSWER' }]"
                    :filter-method="filterType"
                    filter-placement="bottom-end"
                    :filter-multiple="true">
                    <template slot-scope="scope">
                        <bk-tag theme="info" type="filled">
                            {{questionType(scope.row.types)}}
                        </bk-tag>
                    </template>
                </bk-table-column>
                <bk-table-column label="操作" width="200">
                    <template slot-scope="props">
                        <bk-button theme="primary" text @click="deleteQuestion(props.row)">删除</bk-button>
                    </template>
                </bk-table-column>
            </bk-table>
        </div>
    </div>
</template>
<script>
    import QuestionRadio from '../../../../components/question/QuestionRadio.vue'
    import QuestionMulti from '../../../../components/question/QuestionMulti.vue'
    import QuestionJudge from '../../../../components/question/QuestionJudge.vue'
    import QuestionShort from '../../../../components/question/QuestionShort.vue'
    import QuestionFill from '../../../../components/question/QuestionFill.vue'
    import ChapterManage from '../../../../components/chapter/ChapterManage.vue'
    import QuestionImport from '../../../../components/question/QuestionImport.vue'
    export default {
        name: 'set_question_detail',
        components: {
            QuestionRadio,
            QuestionMulti,
            QuestionJudge,
            QuestionShort,
            QuestionFill,
            ChapterManage,
            QuestionImport
        },
        data () {
            return {
                editQuestion: {
                    visable: false,
                    Question: null
                },
                pagination: {
                    current: 1,
                    count: 500,
                    limit: 10
                },
                config: {
                    message: null,
                    theme: 'error',
                    offset: 80
                },
                Dict: {
                    'SINGLE': 'QuestionRadio',
                    'MULTIPLE': 'QuestionMulti',
                    'COMPLETION': 'QuestionFill',
                    'JUDGE': 'QuestionJudge',
                    'SHORT_ANSWER': 'QuestionShort'
                },
                componentKey: 0,
                componentKey1: 0,
                componentKey2: 0,
                curChapter: [],
                curChapterId: null,
                chapterFilters: [],
                chapterList: [],
                selection: [],
                questionList: [],
                showQuestionList: [],
                panels: [
                    { name: 'QuestionImport', label: '批量导入', count: 10 },
                    { name: 'QuestionRadio', label: '单选题', count: 20 },
                    { name: 'QuestionMulti', label: '多选题', count: 30 },
                    { name: 'QuestionJudge', label: '判断题', count: 40 },
                    { name: 'QuestionFill', label: '填空题', count: 50 },
                    { name: 'QuestionShort', label: '简答题', count: 60 }
                ],
                active: 'QuestionImport'
            }
        },
        computed: {
            curType: function () {
                if (this.active === 'QuestionRadio') {
                    return ['SINGLE']
                } else if (this.active === 'QuestionMulti') {
                    return ['MULTIPLE']
                } else if (this.active === 'QuestionJudge') {
                    return ['JUDGE']
                } else if (this.active === 'QuestionFill') {
                    return ['COMPLETION']
                } else if (this.active === 'QuestionShort') {
                    return ['SHORT_ANSWER']
                } else {
                    return []
                }
            },
            courseId: function () {
                return this.$store.state.currentCourseId
            },
            showQuestionList1: function () {
                const pageNumber = Math.ceil(this.pagination.count / this.pagination.limit)
                const start = (this.pagination.current - 1) * this.pagination.limit
                return this.pagination.current === pageNumber ? this.showQuestionList.slice(start, start + this.pagination.limit) : this.showQuestionList.slice(start, start + this.pagination.limit)
            }
        },
        watch: {
            courseId: function (newVal, oldVal) {
                this.getChapterList()
            },
            questionList: function (newVal, oldVal) {
                this.showQuestionList = newVal
                if (this.curType.length > 0) {
                    const filteredQuestionList = []
                    this.questionList.forEach(question => {
                        if (question.types === this.curType[0]) {
                            filteredQuestionList.push(question)
                        }
                    })
                    this.showQuestionList = filteredQuestionList
                    this.pagination.count = filteredQuestionList.length
                } else {
                    this.pagination.count = this.questionList.length
                }
                this.pagination.current = 1
            }
        },
        created () {
            this.getChapterList()
            this.componentKey1 = this.componentKey1 + 1
        },
        methods: {
            async getChapterList () {
                this.$http.get('/course/get_chapter_list/', { params: { course_id: this.courseId } }).then(res => {
                    this.chapterList = res.data
                    this.chapterFilters = []
                    this.chapterList.forEach(item => {
                        this.chapterFilters.push({
                            text: item.chapter_name,
                            value: item.id
                        })
                    })
                    this.curChapterId = null
                    this.getQuestionList()
                })
            },
            async operateChapter (chapterList) {
                this.$http.post('/course/operate_chapter/', { course_id: this.courseId, chapter_list: chapterList }).then(res => {
                    if (res.result) {
                        this.config.theme = 'success'
                        this.config.message = '修改成功！'
                        this.$bkMessage(this.config)
                    } else {
                        this.config.theme = 'error'
                        this.config.message = res.message
                        this.$bkMessage(this.config)
                    }
                    this.getChapterList()
                })
            },
            async getQuestionList () {
                this.$http.get('/course/get_question_list/', { params: { course_id: this.courseId, chapter_id: this.curChapterId } }).then(res => {
                    this.questionList = res.data
                    this.componentKey = this.componentKey + 1
                })
            },
            async setQuestion (method, item) {
                if (method === 'append') {
                    if (this.curChapterId) {
                        this.$http.post('/course/teacher_set_question/', {
                            course_id: this.courseId,
                            question: item.question,
                            chapter_id: this.curChapterId,
                            types: item.types,
                            option_A: item.option_A,
                            option_B: item.option_B,
                            option_C: item.option_C,
                            option_D: item.option_D,
                            option_E: item.option_E,
                            answer: item.answer,
                            explain: item.explain
                        }).then(res => {
                            if (res.result) {
                                this.config.theme = 'success'
                                this.config.message = '上传成功！'
                            } else {
                                this.config.theme = 'error'
                                this.config.message = res.message
                            }
                            this.$bkMessage(this.config)
                            this.componentKey2 = this.componentKey2 + 1
                            this.getQuestionList()
                        })
                    } else {
                        this.config.theme = 'error'
                        this.config.message = '章节为空！先选择章节再进行出题'
                        this.$bkMessage(this.config)
                    }
                } else if (method === 'delete') {
                    if (item.length > 0) {
                        this.$http.delete('/course/teacher_set_question/', { params: { course_id: this.courseId, question_id_list: JSON.stringify(item) } }).then(res => {
                            if (res.result) {
                                this.config.theme = 'success'
                                this.config.message = '删除成功！'
                            } else {
                                this.config.theme = 'error'
                                this.config.message = res.message
                            }
                            this.$bkMessage(this.config)
                            this.getQuestionList()
                        })
                    }
                } else if (method === 'update') {
                    this.$http.put('/course/teacher_set_question/', {
                        course_id: this.courseId,
                        question_id: item.question_id,
                        question: item.question,
                        types: item.types,
                        option_A: item.option_A,
                        option_B: item.option_B,
                        option_C: item.option_C,
                        option_D: item.option_D,
                        option_E: item.option_E,
                        answer: item.answer,
                        explain: item.explain
                    }).then(res => {
                        if (res.result) {
                            this.config.theme = 'success'
                            this.config.message = '修改成功！'
                        } else {
                            this.config.theme = 'error'
                            this.config.message = res.message
                        }
                        this.$bkMessage(this.config)
                        this.getQuestionList()
                        this.editQuestion.visable = false
                    })
                }
            },
            createQuestion (item) {
                this.setQuestion('append', item)
            },
            filterType (value, row) {
                return row.types === value
            },
            filterChapter (value, row) {
                return row.chapter_id === value
            },
            filterHandler (value, row, column) {
                const property = column['property']
                return row[property] === value
            },
            handleSelectChange (selection, row) {
                this.selection = selection
            },
            handleFilterChange (filters) {
                let curType = []
                for (const item in filters) {
                    curType = filters[item]
                }
                if (curType.length > 0) {
                    const filteredQuestionList = []
                    curType.forEach(types => {
                        this.questionList.forEach(question => {
                            if (question.types === types) {
                                filteredQuestionList.push(question)
                            }
                        })
                    })
                    this.showQuestionList = filteredQuestionList
                    this.pagination.count = filteredQuestionList.length
                } else {
                    this.showQuestionList = this.questionList
                    this.pagination.count = this.questionList.length
                }
            },
            handleRowClick (row, event, column, rowIndex, columnIndex) {
                if (columnIndex !== 4) {
                    this.editQuestion.Question = row
                    this.editQuestion.visable = true
                }
            },
            handleTabChange (name) {
                this.componentKey += 1
                const filteredQuestionList = []
                if (this.curType.length > 0) {
                    this.questionList.forEach(question => {
                        if (question.types === this.curType[0]) {
                            filteredQuestionList.push(question)
                        }
                    })
                    this.showQuestionList = filteredQuestionList
                    this.pagination.count = this.showQuestionList.length
                } else {
                    this.showQuestionList = this.questionList
                    this.pagination.count = this.questionList.length
                }
                this.pagination.current = 1
            },
            handleSelected (value, option) {
                this.getQuestionList()
                this.curChapter = []
                this.curChapter.push(value)
                this.curChapterid = value
                this.componentKey += 1
            },
            handleChapterClear (oldVal) {
                this.curChapterid = null
                this.getQuestionList()
            },
            deleteQuestion (row) {
                const questionIdList = []
                questionIdList.push(row.question_id)
                this.setQuestion('delete', questionIdList)
            },
            deleteQuestions (row) {
                const questionIdList = []
                this.selection.forEach(question => {
                    questionIdList.push(question.question_id)
                })
                this.setQuestion('delete', questionIdList)
            },
            ToManageChapter () {
                this.$router.push({
                    name: 'manage_chapter_index'
                })
            },
            updateChapter (item, saved) {
                if (saved) {
                    this.operateChapter(item)
                } else {
                    this.componentKey1 = this.componentKey1 + 1
                }
            },
            updateQuestion (item) {
                this.setQuestion('update', item)
            },
            questionType (type) {
                if (type === 'SINGLE') {
                    return '单选题'
                } else if (type === 'MULTIPLE') {
                    return '多选题'
                } else if (type === 'JUDGE') {
                    return '判断题'
                } else if (type === 'COMPLETION') {
                    return '填空题'
                } else if (type === 'SHORT_ANSWER') {
                    return '简答题'
                } else {
                    return []
                }
            },
            handlePageChange (newPage) {
                this.pagination.current = newPage
            },
            handlePageLimitChange (limit) {
                this.pagination.current = 1
                this.pagination.limit = limit
            }
        }
    }
</script>
<style lang="postcss" scoped>
    .create_question {
        height: 100%;
        width: 100%;
        overflow: scroll;
    }
    .create_question::-webkit-scrollbar {
        display: none;
    }
    .create_question::-webkit-scrollbar {
    /*滚动条整体样式*/
    width : 5px;  /*高宽分别对应横竖滚动条的尺寸*/
    height: 1px;
    }
    .create_question::-webkit-scrollbar-thumb {
    /*滚动条里面小方块*/
    border-radius: 10px;
    box-shadow   : inset 0 0 5px rgb(255, 255, 255);
    background   : #868686;
    }
    .create_question::-webkit-scrollbar-track {
    /*滚动条里面轨道*/
    box-shadow   : inset 0 0 5px rgba(0, 0, 0, 0.2);
    border-radius: 10px;
    background   : #ededed;
    }
    .questions {
    }
</style>
