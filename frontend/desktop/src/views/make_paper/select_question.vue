<template>
    <div id="my" style="display:flex;">
        <bk-dialog v-model="editQuestion.visable" width="1200" :draggable="false" :show-footer="false">
            <component v-if="editQuestion.visable" :is="Dict[editQuestion.Question.types]" :info="editQuestion.Question" @updateQuestion="updateQuestion" :editable="true" :readonly="true"></component>
        </bk-dialog>
        <bk-dialog v-model="previewsetting.visible"
            width="720"
            :position="previewsetting.position"
            title="试卷预览">
            <div v-for="questiontitle in papertree[0].children" :key="questiontitle.name">
                <h3>{{questiontitle.name}}</h3>
                <bk-card class="radio-common" :title="`${index + 1}.${item.dialogdata.question} （${item.score}分）`" v-for="(item,index) in questiontitle.children" :key="index" :border="false">
                    <bk-radio-group v-if="item.dialogdata.types === 'SINGLE'" class="radio-common">
                        <bk-radio value="A" :disabled="true">
                            A：{{ item.dialogdata.option_A }}
                        </bk-radio>
                        <bk-radio value="B" :disabled="true">
                            B：{{ item.dialogdata.option_B }}
                        </bk-radio>
                        <bk-radio value="C" :disabled="true">
                            C：{{ item.dialogdata.option_C }}
                        </bk-radio>
                        <bk-radio value="D" :disabled="true">
                            D：{{ item.dialogdata.option_D }}
                        </bk-radio>
                    </bk-radio-group>
                    <bk-radio-group v-if="item.dialogdata.types === 'MULTIPLE'" class="radio-common">
                        <bk-radio value="A" :disabled="true">
                            A：{{ item.dialogdata.option_A }}
                        </bk-radio>
                        <bk-radio value="B" :disabled="true">
                            B：{{ item.dialogdata.option_B }}
                        </bk-radio>
                        <bk-radio value="C" :disabled="true">
                            C：{{ item.dialogdata.option_C }}
                        </bk-radio>
                        <bk-radio value="D" :disabled="true">
                            D：{{ item.dialogdata.option_D }}
                        </bk-radio>
                        <bk-radio value="E" :disabled="true">
                            E：{{ item.dialogdata.option_E }}
                        </bk-radio>
                    </bk-radio-group>
                </bk-card>
            </div>
        </bk-dialog>
        <bk-dialog v-model="dialogsetting.visible"
            width="300"
            :position="dialogsetting.position"
            @confirm="confirmtitle"
            title="添加大题">
            <bk-select :disabled="false" v-model="titilevalue" style="width: 250px;"
                ext-cls="select-custom"
                ext-popover-cls="select-popover-custom"
                searchable>
                <bk-option v-for="option in paperquestiontype"
                    :key="option.id"
                    :id="option.id"
                    :name="option.name">
                </bk-option>
            </bk-select>
        </bk-dialog>
        <div class="left">
            <div>
                <span style="display:inline-block;">所属大题：</span>
                <bk-select style="width: 200px;display:inline-block" class="type-select" v-model="questionparameter.questiontype" searchable>
                    <bk-option v-for="option in papertree[0].children"
                        :key="option.id"
                        :id="option.name"
                        :name="option.name">
                    </bk-option>
                </bk-select>
                <span style="display:inline-block">请设置分数：</span>
                <bk-input style="width:200px;" type="number" :max="100" :min="0" :precision="precision" v-model="questionparameter.score"></bk-input>
                <bk-button theme="primary" @click="popquestion" :disabled="popbutton">录入卷子</bk-button>
                <bk-button theme="primary" @click="moveout" :disabled="moveoutbutton">移出卷子</bk-button>
            </div>
            <bk-table
                ref="table"
                style="width:800px"
                :height="480"
                :data="questionlist"
                :row-class-name="tableRowClassName"
                :row-style="tableRowStyle"
                @row-click="handleRowClick"
                @selection-change="handleSelectionChange">
                <bk-table-column
                    :selectable="selectEnable"
                    type="selection"
                    width="30"></bk-table-column>
                <bk-table-column label="题目" prop="question"></bk-table-column>
                <bk-table-column
                    :filters="typeFilters"
                    :filter-method="typeFilterMethod"
                    label="题目类型"
                    prop="type"></bk-table-column>
                <bk-table-column
                    :filters="statusFilters"
                    :filter-method="statusFilterMethod"
                    label="状态"
                    prop="status"></bk-table-column>
            </bk-table>
        </div>
        <div>
            <div class="right-top">
                <question-title-manage :questiontitles="questionTitleList" @updateQuestionTitle="updateQuestionTitle"></question-title-manage>
            </div>
            <div class="right-bottom">
                <bk-tree
                    ref="tree"
                    :data="papertree"
                    :node-key="'id'"
                    :draggable="true"
                    :drag-sort="dragSort"
                    :has-border="true"
                    :tpl="tpl"
                    @on-click="clicknode">
                </bk-tree>
                <bk-button style="margin-left:10px;margin-right:10px" theme="primary" @click="previewsetting.visible = true">预览试卷</bk-button>
                <bk-button theme="primary" :disabled="!saveble" :loading="loadingbutton" @click="savepaper">保存试卷</bk-button>
            </div>
        </div>
    </div>
</template>

<script>
    import QuestionRadio from '../../components/question/QuestionRadio.vue'
    import QuestionMulti from '../../components/question/QuestionMulti.vue'
    import QuestionJudge from '../../components/question/QuestionJudge.vue'
    import QuestionShort from '../../components/question/QuestionShort.vue'
    import QuestionFill from '../../components/question/QuestionFill.vue'
    import QuestionTitleManage from '../../components/question-title/QuestionTitleManage.vue'
    import CircularJSON from 'circular-json'
    export default {
        components: {
            QuestionRadio,
            QuestionMulti,
            QuestionJudge,
            QuestionShort,
            QuestionFill,
            QuestionTitleManage
        },
        data () {
            return {
                previewsetting: {
                    visible: false,
                    position: {
                        top: 25
                    }
                },
                Dict: {
                    'SINGLE': 'QuestionRadio',
                    'MULTIPLE': 'QuestionMulti',
                    'COMPLETION': 'QuestionFill',
                    'JUDGE': 'QuestionJudge',
                    'SHORT_ANSWER': 'QuestionShort'
                },
                editQuestion: {
                    visable: false,
                    Question: null
                },
                papertree: [
                    {
                        name: '试卷',
                        title: '试卷',
                        flag: 0, // 判断需要显示‘+’还是‘-’。0显示‘+’、1显示‘-’
                        expanded: true,
                        openedIcon: 'icon-folder-open',
                        closedIcon: 'icon-folder',
                        id: 0,
                        Id: undefined,
                        children: [
                        ]
                    }
                ],
                paperinit: [],
                questionlist: [],
                existlist: [],
                dragSort: true,
                dialogsetting: {
                    visible: false,
                    position: { top: 100 }
                },
                sidesliderSettings: {
                    isShow: false,
                    title: '大题信息'
                },
                questionparameter: {
                    questiontype: undefined,
                    score: 0
                },
                append: {
                    questiontitle: undefined
                },
                paperquestiontype: [
                ],
                paperquestiontypeMap: {}, // 题目名到题目id的映射
                typeFilters: [
                    {
                        text: '单选题',
                        value: '单选题'
                    },
                    {
                        text: '多选题',
                        value: '多选题'
                    },
                    {
                        text: '填空题',
                        value: '填空题'
                    },
                    {
                        text: '判断题',
                        value: '判断题'
                    },
                    {
                        text: '简答题',
                        value: '简答题'
                    }
                ],
                statusFilters: [
                    {
                        text: '未录入',
                        value: '未录入'
                    },
                    {
                        text: '已录入',
                        value: '已录入'
                    }
                ],
                titilevalue: undefined,
                firstrow: undefined,
                popbutton: true,
                moveoutbutton: true,
                isdiabled: true,
                loadingbutton: false,
                // saveble: false,
                questionTitleList: []
            }
        },
        computed: {
            CourseId: function () {
                return this.$store.state.currentCourseId
            },
            saveble: function () {
                return this.isModified(this.paperinit, this.papertree[0])
            }
        },
        watch: {
            firstrow: {
                handler () {
                    if (this.firstrow === '未录入') {
                        this.popbutton = false
                        this.moveoutbutton = true
                    }
                    if (this.firstrow === '已录入') {
                        this.popbutton = true
                        this.moveoutbutton = false
                    }
                    if (this.firstrow === undefined) {
                        this.popbutton = true
                        this.moveoutbutton = true
                    }
                }
            },
            CourseId: {
                handler () {
                    this.$router.push({
                        name: 'displaypaper'
                    })
                }
            }
        },
        created () {
            if (sessionStorage.getItem('paperinfo')) {
                const paperinit = JSON.parse(sessionStorage.getItem('paperinit'))
                const paperinfo = CircularJSON.parse(sessionStorage.getItem('paperinfo'))
                this.paperinit = paperinit
                this.papertree = paperinfo
                this.existlist = JSON.parse(sessionStorage.getItem('existlist'))
                this.getquestiontitle2()
                this.getquetionlist()
                sessionStorage.removeItem('paperinfo')
                sessionStorage.removeItem('existlist')
                sessionStorage.removeItem('paperinit')
            } else {
                this.getquestiontitle()
            }
            window.addEventListener('beforeunload', () => {
                sessionStorage.setItem('paperinfo', CircularJSON.stringify(this.papertree))
                sessionStorage.setItem('existlist', JSON.stringify(this.existlist))
                sessionStorage.setItem('paperinit', JSON.stringify(this.paperinit))
            })
        },
        methods: {
            isModified (oldval, newval) {
                const flag = { val: 0 }
                if (oldval.length !== newval.children.length) { // 大题数量是否相同
                    flag.val = 1
                } else {
                    for (let i = 0; i < oldval.length; i++) {
                        if (oldval[i].Id !== newval.children[i].Id) { // 大题是否相同
                            flag.val = 1
                            break
                        } else {
                            if (oldval[i].children.length !== newval.children[i].children.length) { // 大题下的题目数量是否相同
                                flag.val = 1
                                break
                            } else {
                                for (let j = 0; j < oldval[i].children.length; j++) {
                                    if (oldval[i].children[j].id !== newval.children[i].children[j].id) { // 大题下的题目是否相同
                                        flag.val = 1
                                        break
                                    }
                                }
                            }
                        }
                    }
                }
                if (flag.val === 1) {
                    return true
                } else {
                    return false
                }
            },
            clicknode (node) {
                if (!node.children) {
                    this.editQuestion.Question = node.dialogdata
                    this.editQuestion.visable = true
                }
            },
            handleRowClick (row, event, column, rowIndex, columnIndex) {
                this.editQuestion.Question = row
                this.editQuestion.visable = true
            },
            tpl (node, ctx) {
                const titleClass = 'node-title'
                if (node.flag === 1) {
                    return <span>
                    <span class="delete-button" onClick={() => this.deltitlenode(node)}>-</span>
                    <span class={titleClass} domPropsInnerHTML={node.title} onClick={() => this.clicknode(node)}></span>
                    </span>
                }
                if (node.flag === 0) {
                    return <span>
                    <span class="add-button" onClick={() => this.addtitlenode()}>+</span>
                    <span class={titleClass} domPropsInnerHTML={node.title}></span>
                </span>
                }
            },
            deltitlenode (node) {
                if (node.children === undefined) { // 没有children的为题目
                    this.delquestion(node.id)
                    this.$refs.tree.delNode(node.parent, node)
                } else {
                    if (node.children.length > 2) { // 大题下面的题目多于2道时，才会提醒
                        const that = this
                        this.$bkInfo({
                            type: 'warning',
                            title: '确认要删除？',
                            confirmFn: function () {
                                node.children.forEach(item => {
                                    that.delquestion(item.id)
                                })
                                that.$refs.tree.delNode(node.parent, node)
                            },
                            cancelFn: function () {
                                node.expanded = true
                            }
                        })
                    } else {
                        node.children.forEach(item => {
                            this.delquestion(item.id)
                        })
                        this.$refs.tree.delNode(node.parent, node)
                    }
                }
            },
            async delquestion (id) { // 将题目状态由已录入改成未录入
                for (const i in this.questionlist) {
                    if (id === this.questionlist[i].QuestionId) {
                        this.existlist.splice(this.existlist.indexOf(id), 1)
                        this.questionlist[i].status = '未录入'
                        break
                    }
                }
            },
            addtitlenode () {
                this.dialogsetting.visible = true
            },
            confirmtitle () {
                const tmp = { val: '' }
                for (const i in this.paperquestiontype) {
                    if (this.titilevalue === this.paperquestiontype[i].id) {
                        tmp.val = this.paperquestiontype[i].name
                        break
                    }
                }
                this.papertree[0].children.push({
                    name: tmp.val,
                    title: tmp.val,
                    flag: 1, // 判断需要显示‘+’还是‘-’。0显示‘+’、1显示‘-’
                    openedIcon: 'icon-folder-open',
                    closedIcon: 'icon-folder',
                    expanded: true,
                    id: -this.titilevalue,
                    Id: this.titilevalue,
                    children: []
                })
                this.titilevalue = undefined
                this.papertree[0].expanded = true
            },
            judge () { // 判断是否和第一个选择的是否相同
                const flag = { value: 0 }
                for (const i in this.Selections) {
                    if (this.Selections[0].status !== this.Selections[i].status) {
                        flag.value = 1
                        break
                    }
                }
                if (flag.value === 1) {
                    this.$refs.table.clearSelection()
                    this.Selections = undefined
                    this.$bkMessage({
                        message: '所选择题目状态不相同，已自动取消选择',
                        theme: 'warning'
                    })
                }
            },
            selectEnable (row, index) { // 判断题目是否能选择
                if (this.firstrow !== undefined) {
                    if (row.status !== this.firstrow) {
                        return false
                    } else {
                        return true
                    }
                } else {
                    return true
                }
            },
            clearFilter () { // 清空过滤条件
                this.$refs.table.clearFilter()
            },
            typeFilterMethod (value, row, column) { // 通过题型过滤
                const property = column.property
                return row[property] === value
            },
            statusFilterMethod (value, row, column) { // 通过状态过滤
                const property = column.property
                return row[property] === value
            },
            handleSelectionChange (val) {
                this.Selections = val
                if (this.Selections.length > 0) {
                    this.firstrow = this.Selections[0].status
                } else {
                    this.firstrow = undefined
                }
                this.judge()
            },
            popquestion () { // 录入卷子
                const flag = { value: 0 }
                if (this.Selections.length > 0) {
                    if (this.questionparameter.questiontype === undefined) {
                        this.$bkInfo({
                            type: 'warning',
                            title: '请先选择所属题型'
                        })
                        flag.value = 1
                    } else if (this.questionparameter.score === 0) {
                        this.$bkInfo({
                            type: 'warning',
                            title: '请设置分数'
                        })
                        flag.value = 1
                    }
                } else {
                    this.$bkInfo({
                        type: 'warning',
                        title: '请先选择题目'
                    })
                }
                if (flag.value === 0) {
                    this.confirmquestion()
                }
            },
            moveout () { // 将题目移出卷子
                const flag = { value: 0 }
                for (const j in this.Selections) {
                    flag.value = 0
                    for (const i in this.papertree[0].children) {
                        for (const t in this.papertree[0].children[i].children) {
                            if (this.papertree[0].children[i].children[t].id === this.Selections[j].QuestionId) {
                                this.existlist.splice(this.existlist.indexOf(this.Selections[j].QuestionId), 1)
                                this.papertree[0].children[i].children.splice(t, 1)
                                this.Selections[j].status = '未录入'
                                flag.value = 1
                                break
                            }
                        }
                        if (flag.value === 1) {
                            break
                        }
                    }
                }
                this.firstrow = undefined
                this.$refs.table.clearSelection()
            },
            confirmquestion () {
                for (const i in this.papertree[0].children) {
                    if (this.questionparameter.questiontype === this.papertree[0].children[i].name) {
                        for (const k in this.Selections) {
                            this.existlist.push(this.Selections[k].QuestionId)
                            this.Selections[k].status = '已录入'
                            if (this.Selections[k].question.length > 14) {
                                const titledisplay = this.Selections[k].question.substr(0, 13) + '...'
                                this.papertree[0].children[i].children.push({
                                    id: this.Selections[k].QuestionId,
                                    title: titledisplay,
                                    name: this.Selections[k].question,
                                    flag: 1,
                                    icon: 'icon-file',
                                    score: this.questionparameter.score,
                                    dialogdata: {
                                        explain: this.Selections[k].explain,
                                        option_A: this.Selections[k].option_A,
                                        option_B: this.Selections[k].option_B,
                                        option_C: this.Selections[k].option_C,
                                        option_D: this.Selections[k].option_D,
                                        option_E: this.Selections[k].option_E,
                                        answer: this.Selections[k].answer,
                                        types: this.Selections[k].types,
                                        question: this.Selections[k].question
                                    }
                                })
                            } else {
                                this.papertree[0].children[i].children.push({
                                    id: this.Selections[k].QuestionId,
                                    title: this.Selections[k].question,
                                    name: this.Selections[k].question,
                                    flag: 1,
                                    icon: 'icon-file',
                                    score: this.questionparameter.score,
                                    dialogdata: {
                                        explain: this.Selections[k].explain,
                                        option_A: this.Selections[k].option_A,
                                        option_B: this.Selections[k].option_B,
                                        option_C: this.Selections[k].option_C,
                                        option_D: this.Selections[k].option_D,
                                        option_E: this.Selections[k].option_E,
                                        answer: this.Selections[k].answer,
                                        types: this.Selections[k].types,
                                        question: this.Selections[k].question
                                    }
                                })
                            }
                        }
                        this.firstrow = undefined
                        this.$refs.table.clearSelection()
                    }
                }
            },
            modifiytype () {
                this.sidesliderSettings.isShow = true
            },
            tableRowStyle ({ row, rowIndex }) {
                if (row.status === '已录入') {
                    const style = {
                        'background-color': '#E1ECFF'
                    }
                    return style
                }
            },
            async savepaper () { // 保存试卷
                try {
                    this.loadingbutton = true
                    await new Promise(resolve => {
                        setTimeout(() => {
                            resolve('成功')
                        }, 1200)
                    })
                    const data = []
                    for (const i in this.papertree[0].children) {
                        const quesitonlist = []
                        const scorelist = []
                        const tmp = {}
                        for (const j in this.papertree[0].children[i].children) {
                            quesitonlist.push(this.papertree[0].children[i].children[j].id)
                            scorelist.push(this.papertree[0].children[i].children[j].score)
                        }
                        this.$set(tmp, this.papertree[0].children[i].Id, [quesitonlist, scorelist])
                        data.push(tmp)
                    }
                    this.updatepaper(data)
                    this.loadingbutton = false
                    return true
                } catch (e) {
                    return false
                }
            },
            async getquetionlist () { // 获得题目
                this.$http.get('/course/get_question_list/', { params: { course_id: this.CourseId, chapter_id: this.$route.query.chapterid } }).then(res => {
                    this.questionlist = []
                    if (res.data.length !== 0) {
                        const tmp = {
                            SINGLE: '单选题',
                            MULTIPLE: '多选题',
                            JUDGE: '判断题',
                            COMPLETION: '填空题',
                            SHORT_ANSWER: '简答题'
                        }
                        for (const i in res.data) {
                            if (this.existlist.indexOf(res.data[i].question_id) === -1) { // 没有找到
                                this.questionlist.push({
                                    explain: res.data[i].explain,
                                    option_A: res.data[i].option_A,
                                    option_B: res.data[i].option_B,
                                    option_C: res.data[i].option_C,
                                    option_D: res.data[i].option_D,
                                    option_E: res.data[i].option_E,
                                    answer: res.data[i].answer,
                                    types: res.data[i].types,
                                    question: res.data[i].question,
                                    QuestionId: res.data[i].question_id,
                                    type: tmp[res.data[i].types],
                                    status: '未录入'
                                })
                            } else {
                                this.questionlist.push({
                                    explain: res.data[i].explain,
                                    option_A: res.data[i].option_A,
                                    option_B: res.data[i].option_B,
                                    option_C: res.data[i].option_C,
                                    option_D: res.data[i].option_D,
                                    option_E: res.data[i].option_E,
                                    answer: res.data[i].answer,
                                    types: res.data[i].types,
                                    QuestionId: res.data[i].question_id,
                                    question: res.data[i].question,
                                    type: tmp[res.data[i].types],
                                    status: '已录入'
                                })
                            }
                        }
                    }
                })
            },
            async operateQuestionTitle (questionTitleList) {
                this.$http.post('/course/question_title/', { course_id: this.$store.state.currentCourseId, custom_type_info: questionTitleList }).then(res => {
                    if (res.result) {
                        this.$bkMessage({
                            message: '修改成功！',
                            theme: 'success'
                        })
                    } else {
                        this.$bkMessage({
                            message: res.message,
                            theme: 'error'
                        })
                    }
                }).then(res => {
                    this.$http.get('/course/question_title/', { params: { course_id: this.CourseId } }).then(res => {
                        if (res.result === true) {
                            this.paperquestiontype = []
                            this.questionTitleList = []
                            for (const i in res.data.custom_types) {
                                this.$set(this.paperquestiontypeMap, res.data.custom_types[i].custom_type_name, res.data.custom_types[i].id)
                                this.paperquestiontype.push({
                                    name: res.data.custom_types[i].custom_type_name,
                                    id: res.data.custom_types[i].id
                                })
                                this.questionTitleList.push({
                                    custom_type_name: res.data.custom_types[i].custom_type_name,
                                    custom_type_id: res.data.custom_types[i].id
                                })
                            }
                        }
                    }).then(res => {
                        this.papertree[0].children.forEach(item1 => {
                            this.paperquestiontype.forEach(item2 => {
                                if (item1.Id === item2.id && item1.name !== item2.name) {
                                    item1.title = item2.name
                                    item1.name = item2.name
                                }
                            })
                        })
                    })
                })
            },
            async getquestiontitle2 () {
                this.$http.get('/course/question_title/', { params: { course_id: this.CourseId } }).then(res => {
                    if (res.result === true) {
                        this.paperquestiontype = []
                        this.questionTitleList = []
                        for (const i in res.data.custom_types) {
                            this.$set(this.paperquestiontypeMap, res.data.custom_types[i].custom_type_name, res.data.custom_types[i].id)
                            this.paperquestiontype.push({
                                name: res.data.custom_types[i].custom_type_name,
                                id: res.data.custom_types[i].id
                            })
                            this.questionTitleList.push({
                                custom_type_name: res.data.custom_types[i].custom_type_name,
                                custom_type_id: res.data.custom_types[i].id
                            })
                        }
                    }
                })
            },
            async getquestiontitle () { // 获得大题名字
                this.$http.get('/course/question_title/', { params: { course_id: this.CourseId } }).then(res => {
                    if (res.result === true) {
                        this.paperquestiontype = []
                        this.questionTitleList = []
                        for (const i in res.data.custom_types) {
                            this.$set(this.paperquestiontypeMap, res.data.custom_types[i].custom_type_name, res.data.custom_types[i].id)
                            this.paperquestiontype.push({
                                name: res.data.custom_types[i].custom_type_name,
                                id: res.data.custom_types[i].id
                            })
                            this.questionTitleList.push({
                                custom_type_name: res.data.custom_types[i].custom_type_name,
                                custom_type_id: res.data.custom_types[i].id
                            })
                        }
                    }
                }).then(res => {
                    this.getpaperinfo()
                })
            },
            async getpaperinfo () { // 获得试卷信息
                this.$http.get('/course/manage_paper_question_contact/', { params: { course_id: this.CourseId, paper_id: this.$route.query.paperid } }).then(res => {
                    this.existlist = []
                    this.papertree[0].children = []
                    this.paperinit = []
                    this.papertree[0].Id = this.$route.query.paperid
                    if (res.result === true) {
                        for (const i in res.data) {
                            const tmp = []
                            const inittmp = []
                            for (const j in res.data[i]) {
                                this.existlist.push(res.data[i][j].question_id)
                                inittmp.push({
                                    id: res.data[i][j].question_id
                                })
                                if (res.data[i][j].question.length > 14) {
                                    const titledisplay = res.data[i][j].question.substr(0, 13) + '...'
                                    tmp.push({
                                        id: res.data[i][j].question_id,
                                        title: titledisplay,
                                        name: res.data[i][j].question,
                                        flag: 1, // 判断需要显示‘+’还是‘-’。0显示‘+’、1显示‘-’
                                        icon: 'icon-file',
                                        score: res.data[i][j].score,
                                        dialogdata: {
                                            explain: res.data[i][j].explain,
                                            option_A: res.data[i][j].option_A,
                                            option_B: res.data[i][j].option_B,
                                            option_C: res.data[i][j].option_C,
                                            option_D: res.data[i][j].option_D,
                                            option_E: res.data[i][j].option_E,
                                            answer: res.data[i][j].answer,
                                            types: res.data[i][j].types,
                                            question: res.data[i][j].question
                                        }
                                    })
                                } else {
                                    tmp.push({
                                        id: res.data[i][j].question_id,
                                        title: res.data[i][j].question,
                                        name: res.data[i][j].question,
                                        flag: 1, // 判断需要显示‘+’还是‘-’。0显示‘+’、1显示‘-’
                                        icon: 'icon-file',
                                        score: res.data[i][j].score,
                                        dialogdata: {
                                            explain: res.data[i][j].explain,
                                            option_A: res.data[i][j].option_A,
                                            option_B: res.data[i][j].option_B,
                                            option_C: res.data[i][j].option_C,
                                            option_D: res.data[i][j].option_D,
                                            option_E: res.data[i][j].option_E,
                                            answer: res.data[i][j].answer,
                                            types: res.data[i][j].types,
                                            question: res.data[i][j].question
                                        }
                                    })
                                }
                            }
                            this.paperinit.push({
                                Id: this.paperquestiontypeMap[i],
                                children: inittmp
                            })
                            this.papertree[0].children.push({
                                name: i,
                                title: i,
                                openedIcon: 'icon-folder-open',
                                closedIcon: 'icon-folder',
                                expanded: true,
                                flag: 1, // 判断需要显示‘+’还是‘-’。0显示‘+’、1显示‘-’
                                id: -this.paperquestiontypeMap[i], // 树状结构的id，防止与题目id相同出现bug
                                Id: this.paperquestiontypeMap[i],
                                children: tmp
                            })
                        }
                    } else {
                        if (res.message === '卷子没有题目') {
                            this.$bkMessage({
                                message: res.message,
                                theme: 'warning'
                            })
                        } else {
                            this.$bkMessage({
                                message: res.message,
                                theme: 'error'
                            })
                        }
                    }
                }).then(res => {
                    this.getquetionlist()
                })
            },
            async updatepaper (data) { // 保存试卷请求
                this.$http.post('/course/manage_paper_question_contact/', { course_id: this.CourseId, paper_id: this.$route.query.paperid, paper_info: data }).then(res => {
                    if (res.result === true) {
                        this.$bkMessage({
                            message: res.message,
                            theme: 'success'
                        })
                        this.paperinit = []
                        this.papertree[0].children.forEach(item => {
                            const tmp = []
                            item.children.forEach(item0 => {
                                tmp.push({
                                    id: item0.id
                                })
                            })
                            this.paperinit.push({
                                Id: item.Id,
                                children: tmp
                            })
                        })
                    } else {
                        this.$bkMessage({
                            message: res.message,
                            theme: 'error'
                        })
                    }
                })
            },
            updateQuestionTitle (item, saved) {
                if (saved) {
                    this.operateQuestionTitle(item)
                } else {
                    this.$http.get('/course/question_title/', { params: { course_id: this.CourseId } }).then(res => {
                        if (res.result === true) {
                            this.paperquestiontype = []
                            this.questionTitleList = []
                            for (const i in res.data.custom_types) {
                                this.$set(this.paperquestiontypeMap, res.data.custom_types[i].custom_type_name, res.data.custom_types[i].id)
                                this.paperquestiontype.push({
                                    name: res.data.custom_types[i].custom_type_name,
                                    id: res.data.custom_types[i].id
                                })
                                this.questionTitleList.push({
                                    custom_type_name: res.data.custom_types[i].custom_type_name,
                                    custom_type_id: res.data.custom_types[i].id
                                })
                            }
                        }
                    })
                }
            }
        }

    }
</script>

<style>
.monitor-navigation-content {
    overflow-y: scroll;
    overflow-x:auto;
}
#my .right-bottom {
    float: left;
    width: 350px;
    padding-left: 25px;
}
#my .right-top {
    float: left;
    width: 350px;
    padding-left: 0px;
}
#my .left {
    float: left;
}
#my .add-button {
    width: 24px;
    height: 24px;
    line-height: 20px;
    display: inline-block;
    background-color: transparent;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-left: 5px;
    font-size: 12px;
    color: rgb(97, 97, 97);
    text-align: center;
    cursor: pointer;
}
#my .delete-button {
    width: 24px;
    height: 24px;
    line-height: 20px;
    display: inline-block;
    background-color: transparent;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-left: 5px;
    font-size: 12px;
    color: rgb(63, 63, 63);
    text-align: center;
    cursor: pointer;
}
#my .type-select {
    display: inline-block;
    width: 200px;
}
#my .bk-select .bk-select-name {
    display: inline-block;
    line-height: 32px;
    height: 23px;
}
#my .bk-select {
    line-height: 33px;
}
#my .radio-common {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    box-shadow: none;
}
</style>
