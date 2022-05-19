<template>
    <div class="wrapper">
        <div class="navTab">
            <bk-tab :active.sync="active" type="unborder-card">
                <bk-tab-panel
                    v-for="(panel, index) in panels"
                    v-bind="panel"
                    :key="index">
                    <ul v-if="panel.name === 'questionType'" id="questionType">
                        <li>
                            <bk-button theme="default" size="small"
                                title="新增" @click="addSingle" class="mr10 questionType">单选题
                            </bk-button>
                        </li>
                        <li>
                            <bk-button theme="default" size="small"
                                title="新增" @click="addMulti" class="mr10 questionType">多选题
                            </bk-button>
                        </li>
                        <li>
                            <bk-button theme="default" size="small"
                                title="新增" @click="addJudge" class="mr10 questionType">判断题
                            </bk-button>
                        </li>
                        <li>
                            <bk-button theme="default" size="small"
                                title="新增" @click="addShort" class="mr10 questionType">简答题
                            </bk-button>
                        </li>
                    </ul>
                    <div v-if="panel.name === 'outline'">
                        此处生成题目大纲
                        <bk-tree
                            ref="tree1"
                            :data="comName"
                            :node-key="'id'"
                            :has-border="true"
                            @on-click="nodeClickOne"
                            @on-expanded="nodeExpandedOne">
                        </bk-tree>
                    </div>
                </bk-tab-panel>
            </bk-tab>
        </div>
        <div class="questionList">
            <ul :virtual-render="true" id="questionUl">
                <bk-form ref="addform" :model="formData" :rules="rules1" label-width="100">
                    <bk-form-item :required="true" :error-display-type="'normal'" :property="'title'"
                        style="width:360px; display: inline-block" label="任务名称:">
                        <bk-input v-model="formData.title"></bk-input>
                    </bk-form-item>
                    <bk-form-item :required="true" :error-display-type="'normal'" :property="'describe'"
                        style="width:360px; display: inline-block" label="任务描述:">
                        <bk-input v-model="formData.describe"></bk-input>
                    </bk-form-item>
                    <bk-form-item :error-display-type="'normal'" :property="'start_time'"
                        style="width: 350px; display: inline-block" label="开始时间:">
                        <bk-date-picker v-model="formData.start_time" :time-picker-options="timePickerOptions"
                            :type="'datetime'"></bk-date-picker>
                    </bk-form-item>
                    <bk-form-item :error-display-type="'normal'" :property="'end_time'"
                        style="margin-left: 10px; width: 350px; display: inline-block" label="结束时间:">
                        <bk-date-picker v-model="formData.end_time" :time-picker-options="timePickerOptions"
                            :type="'datetime'"></bk-date-picker>
                    </bk-form-item>
                    <bk-form-item :required="true" :error-display-type="'normal'" :property="'types'"
                        style="width:360px; display: inline-block" label="任务类型:">
                        <bk-select style="background: #ffffff"
                            display-tag
                            :auto-height="false"
                            v-model="formData.types">
                            <bk-option v-for="option in typesList"
                                :key="option.value"
                                :id="option.value"
                                :name="option.name">
                            </bk-option>
                        </bk-select>
                    </bk-form-item>
                    <bk-form-item :error-display-type="'normal'" :property="'students_visible'"
                        style="width:360px; display: inline-block;" label="是否可见:">
                        <bk-select style="background: #ffffff"
                            display-tag
                            :auto-height="false"
                            v-model="formData.students_visible">
                            <bk-option v-for="option in visibleRange"
                                :key="option.value"
                                :id="option.value"
                                :name="option.name">
                            </bk-option>
                        </bk-select>
                    </bk-form-item>
                    <bk-form-item :required="true" :error-display-type="'normal'" :property="'students'"
                        style="width:700px; display: inline-block" label="完成学生:">
                        <bk-select style="width: 620px; background: #ffffff"
                            searchable
                            multiple
                            display-tag
                            :auto-height="false"
                            v-model="formData.students">
                            <bk-option v-for="option in studentList"
                                :key="option.id"
                                :id="option.id"
                                :name="option.name">
                            </bk-option>
                        </bk-select>
                    </bk-form-item>
                    <bk-form-item :required="true" :error-display-type="'normal'" :property="'teschers'"
                        style="width:700px; display: inline-block" label="阅卷老师:">
                        <bk-select style="width: 620px; background: #ffffff"
                            searchable
                            multiple
                            display-tag
                            @child-checked="getTeacherWeight"
                            @key-delete="getTeacherWeight"
                            @change="getTeacherWeight"
                            @menu-child-select="getTeacherWeight"
                            :auto-height="false"
                            v-model="formData.teachers">
                            <bk-option v-for="option in teacherList"
                                :key="option.id"
                                :id="option.id"
                                :name="option.name">
                            </bk-option>
                        </bk-select>
                        <bk-table style="margin-top: 15px;"
                            :data="selectedTercher"
                            :size="small">
                            <bk-table-column
                                label="id"
                                column-key="id"
                                prop="id">
                            </bk-table-column>
                            <bk-table-column
                                label="用户名"
                                column-key="name"
                                prop="name">
                            </bk-table-column>
                            <bk-table-column
                                label="权重"
                                column-key="weight"
                                prop="weight">
                            </bk-table-column>
                            <bk-table-column label="操作">
                                <template slot-scope="props">
                                    <bk-button theme="primary" text @click="openEditWeightDialoag(props.row)">设置权重
                                    </bk-button>
                                </template>
                            </bk-table-column>
                        </bk-table>
                    </bk-form-item>

                </bk-form>

                <div v-for="(item,index) in comName" :key="index">
                    <h3>第 {{ index + 1 }} 题</h3>
                    <component
                        :is="item.name"
                        :title="index + 1"
                        @confirms="addQuestionData"
                        @add="openAddDialoag(index)"
                        @func="openDelDialoag(index)">
                    </component>
                </div>
            </ul>
            <bk-button @click="publishPaper.custom.visible = true"
                style="margin-left: 45%; color: #ffffff; background: #88a2ef">确定
            </bk-button>
        </div>
        <!--添加题型Dialog-->
        <bk-dialog v-model="addQuestion.primary.visible"
            theme="primary"
            :mask-close="false"
            :scrollable="true"
            :header-position="addQuestion.primary.headerPosition"
            title="请选择你要添加的题型">
            <bk-button theme="default" size="small"
                title="新增" @click="addSingleQuestion" class="mr10 questionType">单选题
            </bk-button>
            <bk-button theme="default" size="small"
                title="新增" @click="addMultiQuestion" class="mr10 questionType">多选题
            </bk-button>
            <bk-button theme="default" size="small"
                title="新增" @click="addJudgeQuestion" class="mr10 questionType">判断题
            </bk-button>
            <bk-button theme="default" size="small"
                title="新增" @click="addShortQuestion" class="mr10 questionType">简答题
            </bk-button>
        </bk-dialog>
        <!--删除题目Dialog-->
        <bk-dialog v-model="delQuestion.primary.visible"
            theme="primary"
            :mask-close="false"
            :scrollable="true"
            :header-position="delQuestion.primary.headerPosition"
            @confirm="getContent"
            title="提示">
            <h3>是否确定删除此题目？</h3>
        </bk-dialog>
        <!--编辑权重Dialog-->
        <bk-dialog v-model="editWeight.primary.visible"
            ok-text="确定"
            @confirm="checkDialog"
            :auto-close="false"
            :header-position="editWeight.primary.headerPosition"
            title="设置权重">
            <bk-form :model="editForm" :rules="rules" ref="validateForm" :label-width="80">
                <bk-form-item
                    :required="true"
                    :property="'id'"
                    label="id"
                    :error-display-type="'normal'">
                    <bk-tag theme="success">{{editForm.id}}</bk-tag>
                </bk-form-item>
                <bk-form-item
                    :required="true"
                    :property="'name'"
                    label="用户名"
                    :error-display-type="'normal'">
                    <bk-tag theme="info">{{editForm.name}}</bk-tag>
                </bk-form-item>
                <bk-form-item
                    :required="true"
                    :property="'weight'"
                    label="权重"
                    :error-display-type="'normal'">
                    <bk-select :disabled="false" v-model="editForm.weight" style="width: 200px;"
                        ext-cls="select-custom"
                        ext-popover-cls="select-popover-custom"
                        searchable>
                        <bk-option v-for="option in weightList"
                            :key="option.value"
                            :id="option.value"
                            :name="option.name">
                        </bk-option>
                    </bk-select>
                </bk-form-item>
            </bk-form>
        </bk-dialog>
        <!--发布试卷Dialog-->
        <bk-dialog v-model="publishPaper.custom.visible"
            ok-text="确定"
            @confirm="check"
            :auto-close="false"
            :position="publishPaper.custom.position"
            @cancel="$refs.addform.clearError(), formData.start = undefined, formData.end = undefined"
            title="新增试卷">
            <h3>您确定要生成试卷嘛？</h3>
        </bk-dialog>
    </div>
</template>
<script>
    import singleSelection from '../../components/questionCard/singleSelection.vue'
    import multiSelection from '../../components/questionCard/multiSelection.vue'
    import shortAnswer from '../../components/questionCard/shortAnswer.vue'
    import judge from '../../components/questionCard/judge.vue'

    export default {
        components: {
            singleSelection,
            multiSelection,
            shortAnswer,
            judge
        },
        data () {
            return {
                panels: [
                    { name: 'questionType', label: '常用题型', count: 10 },
                    { name: 'outline', label: '大纲', count: 20 }
                ],
                active: 'mission',
                customSettings: {
                    isShow: false,
                    title: '添加问题'
                },
                addQuestion: {
                    primary: {
                        visible: false,
                        headerPosition: 'left'
                    }
                },
                delQuestion: {
                    primary: {
                        visible: false,
                        headerPosition: 'left'
                    }
                },
                editWeight: {
                    primary: {
                        visible: false,
                        headerPosition: 'left'
                    }
                },
                editForm: {
                    name: '',
                    weight: ''
                },
                publishPaper: {
                    custom: {
                        visible: false,
                        position: {
                            top: 100
                        }
                    }
                },
                weight: '',
                weightList: [
                    { value: 0.1, name: '0.1' },
                    { value: 0.2, name: '0.2' },
                    { value: 0.3, name: '0.3' },
                    { value: 0.4, name: '0.4' },
                    { value: 0.5, name: '0.5' },
                    { value: 0.6, name: '0.6' },
                    { value: 0.7, name: '0.7' },
                    { value: 0.8, name: '0.8' },
                    { value: 0.9, name: '0.9' }
                ],
                formData: {
                    project_id: '',
                    questions: [],
                    students: [],
                    teachers: [],
                    questions_detail: [],
                    types: '',
                    title: '',
                    describe: '',
                    start_time: new Date(),
                    end_time: new Date(),
                    judge_teachers_info: [],
                    students_visible: false
                },
                studentList: [],
                teacherList: [],
                comName: [],
                comIndex: '',
                delIndex: '',
                selectedTeacher: [],
                typesList: [
                    {
                        value: 'DAILY',
                        name: '日常任务'
                    },
                    {
                        value: 'ASSESSMENT',
                        name: '考核任务'
                    }
                ],
                visibleRange: [
                    {
                        value: true,
                        name: '是'
                    },
                    {
                        value: false,
                        name: '否'
                    }
                ]
            }
        },
        watch: {
            // 监听当前课程id的变化
            '$store.state.currentCourseId' (newValue) {
                this.course_id = this.$store.state.currentCourseId
                this.getAllUserlist()
                this.getProjectUser()
            }
        },
        created () {
            this.course_id = this.$store.state.currentCourseId
            this.getSelectList()
            this.getTeacherWeight()
        },
        methods: {
            async getTeacherWeight () {
                this.selectedTercher = []
                for (const i in this.formData.teachers) {
                    const item = this.formData.teachers[i]
                    const obj = this.teacherList.find(function (x) {
                        return x.id === item
                    })
                    this.selectedTercher.push(obj)
                    // 数组去重
                    this.selectedTercher = this.unique(this.selectedTercher)
                }
            },
            addQuestionData (obj) {
                this.formData.questions.push(obj.questionData)
                const objIndex = (this.formData.questions || []).findIndex((item) => item.title === obj.questionData.title) + 1
                const details = {
                    'index': objIndex,
                    'score': obj.questionData.score
                }
                this.formData.questions_detail.push(details)
                for (const item of this.formData.questions) {
                    console.log(item)
                    item['project_id'] = this.course_id
                }
            },
            openAddDialoag (index) {
                this.comIndex = index
                this.addQuestion.primary.visible = true
            },
            openDelDialoag (index) {
                this.delIndex = index
                this.delQuestion.primary.visible = true
            },
            openEditWeightDialoag (e) {
                this.editForm.id = e.id
                this.editForm.name = e.name
                this.editForm.weight = ''
                this.editWeight.primary.visible = true
            },
            addSingle () {
                this.comName.push({
                    name: 'singleSelection'
                })
            },
            addSingleQuestion () {
                const insertIndex = this.comIndex + 1
                this.comName.splice(insertIndex, 0, singleSelection)
            },
            addMulti () {
                this.comName.push({
                    name: 'multiSelection'
                })
            },
            addMultiQuestion () {
                const insertIndex = this.comIndex + 1
                this.comName.splice(insertIndex, 0, multiSelection)
            },
            addShort () {
                this.comName.push({
                    name: 'shortAnswer'
                })
            },
            addShortQuestion () {
                const insertIndex = this.comIndex + 1
                this.comName.splice(insertIndex, 0, shortAnswer)
            },
            addJudge () {
                this.comName.push({
                    name: 'judge'
                })
            },
            addJudgeQuestion () {
                const insertIndex = this.comIndex + 1

                this.comName.splice(insertIndex, 0, judge)
            },
            // 删除组件
            getContent () {
                console.log('删除index', this.delIndex)
                this.comName.splice(this.delIndex, 1)
            },
            nodeClickOne (node) {
                console.log(node)
            },
            nodeExpandedOne (node, expanded) {
                console.log(node)
                console.log(expanded)
            },
            //  获取下拉选框学生列表
            getSelectList () {
                console.log('this.course_id', this.course_id)
                this.$http.get(`/api/project-user/${this.course_id}/student/`).then(res => {
                    console.log('res=======student', res)
                    this.studentList = res.data.results
                })

                this.$http.get(`/api/project-user/${this.course_id}/teacher/`).then(res => {
                    // console.log('res=======teacher', res)
                    this.teacherList = res.data.results
                })
            },
            // 确定设置权重
            checkDialog () {
                const id = this.editForm.id
                const obj = this.selectedTercher.find(function (x) {
                    return x.id === id
                })
                obj.weight = this.editForm.weight
                this.editWeight.primary.visible = false
                this.getTeacherWeight()
            },
            // 确定生成试卷
            check () {
                this.selectedTercher.forEach(e => {
                    this.formData.judge_teachers_info.push({ id: e.id, weight: e.weight
                    })
                })
                console.log('this.formData', this.formData)
                this.formData.project_id = this.course_id

                this.$http.post('/api/project-task/', this.formData).then(res => {
                    console.log('生成试卷：', res)
                    if (res.result) {
                        this.$bkMessage({
                            theme: 'success',
                            message: '试卷创建成功'
                        })
                        this.publishPaper.custom.visible = false
                    } else {
                        this.$bkMessage({
                            theme: 'error',
                            message: '试卷创建失败'
                        })
                        this.publishPaper.custom.visible = false
                    }
                })
            },
            // 数组去重
            unique (arr) {
                return Array.from(new Set(arr)) // 利用Array.from将Set结构转换成数组
            }
        }
    }
</script>
<style scoped>
.navTab {
    width: 20%;
    height: 90%;
}

.navTab ul li {
    margin: 20px;
}

#questionType {
    margin-left: 45px;
}

.questionList {
    position: relative;
    background: #f6f6f6;
    width: 78%;
    left: 21%;
    top: -91%;
    height: 98%;

}

.bk-form-item .bk-button {
    margin-top: 20px;
}

.questionType {
    /*margin-left: 45px;*/
    color: #888888;
    border-radius: 3px;
    background-color: #f3f5f7;
}

.questionType:hover {
    background: #dfe1e3;
}

.questionType:active {
    border: #888;
    color: #1f1f1f;
}

.questionList #questionUl {
    height: 93%;
    width: 90%;
    margin: 0 auto;
    right: 1%;
    overflow: auto;
    margin-top: 2% !important;
}

#questionUl::-webkit-scrollbar {
    /*滚动条整体样式*/
    width: 5px; /*高宽分别对应横竖滚动条的尺寸*/
    height: 1px;
}

#questionUl::-webkit-scrollbar-thumb {
    /*滚动条里面小方块*/
    border-radius: 10px;
    box-shadow: inset 0 0 5px rgb(255, 255, 255);
    background: #868686;
}

#questionUl::-webkit-scrollbar-track {
    /*滚动条里面轨道*/
    box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
    border-radius: 10px;
    background: #ededed;
}

.questionList ul {
    height: 100%;
    width: 100%;
    right: 1%;
}
.bk-form-input{
    height: 32px !important;
}
</style>
