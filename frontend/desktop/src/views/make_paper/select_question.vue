<template>
    <div style="display:flex;">
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
        <bk-sideslider :is-show.sync="sidesliderSettings.isShow" :quick-close="true">
            <div slot="header">{{ sidesliderSettings.title }}</div>
            <div slot="content">
                <bk-form :rules="rules" :model="append" ref="appendSection" :label-width="0">
                    <div style="margin-top:5px;margin-bottom:5px">
                        <bk-form-item :error-display-type="'normal'" :property="'questiontitle'">
                            <bk-input v-model="append.questiontitle" ref="appendInput" :clearable="false" style="width:231px;"></bk-input>
                            <bk-button style="display:inline-block" :theme="'primary'" :title="'主要按钮'" icon="plus" class="mr10" @click="addtitle">
                                新增大题
                            </bk-button>
                        </bk-form-item>
                    </div>
                </bk-form>
                <div class="sections">
                    <bk-table
                        :data="paperquestiontype"
                        :size="size"
                        :outer-border="true"
                        :virtual-render="false"
                        :show-header="false"
                        @row-dblclick="handleRowDbclick"
                        @selection-change="handleSelectChange"
                        height="480">
                        <bk-table-column
                            label="章节"
                            prop="name"
                            sortable
                            @row-dblclick="handleRowDbclickSection">
                            <template slot-scope="props">
                                <bk-input
                                    readonly
                                    ref="myinput"
                                    class="input"
                                    v-model="props.row.name"
                                    style="display:inline-block;">
                                </bk-input>
                            </template>
                        </bk-table-column>
                    </bk-table>
                </div>
            </div>
        </bk-sideslider>
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
                <span style="display:inline-block">所属大题：</span>
                <bk-select class="type-select" v-model="questionparameter.questiontype" searchable>
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
                @setCurrentRow="setCurrentRow(row)"
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
        <div class="right">
            <bk-button theme="primary" @click="modifiytype">新增大题</bk-button>
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
            <bk-button theme="primary" @click="savepaper">保存试卷</bk-button>
        </div>
    </div>
</template>

<script>
    import QuestionRadio from '../../components/question/QuestionRadio.vue'
    import QuestionMulti from '../../components/question/QuestionMulti.vue'
    import QuestionJudge from '../../components/question/QuestionJudge.vue'
    import QuestionShort from '../../components/question/QuestionShort.vue'
    import QuestionFill from '../../components/question/QuestionFill.vue'
    export default {
        components: {
            QuestionRadio,
            QuestionMulti,
            QuestionJudge,
            QuestionShort,
            QuestionFill
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
                        id: 1,
                        children: [
                        ]
                    }
                ],
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
                pagination: {
                    current: 1,
                    count: undefined,
                    limit: 15
                },
                questionparameter: {
                    questiontype: undefined,
                    score: 0
                },
                append: {
                    questiontitle: undefined
                },
                rules: {
                    questiontitle: [
                        {
                            required: true,
                            message: '大题名称不能为空！',
                            trigger: 'change'
                        },
                        {
                            max: 10,
                            message: '不能多于10个字符',
                            trigger: 'change'
                        }
                    ]
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
                isdiabled: true
            }
        },
        computed: {
            CourseId: function () {
                return this.$store.state.currentCourseId
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
            this.getquestiontitle()
        },
        methods: {
            clicknode (node) {
                this.editQuestion.Question = node.dialogdata
                this.editQuestion.visable = true
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
                if (node.children.length === 0) {
                    this.$refs.tree.delNode(node.parent, node)
                } else {
                    for (let i = 0; i < node.children.length; i++) {
                        this.$refs.tree.delNode(node.parent, node)
                        this.delquestion(node.children[i].id)
                    }
                }
            },
            async delquestion (id) { // 将题目状态由已录入改成未录入
                for (const i in this.questionlist) {
                    if (id === this.questionlist[i].QuestionId) {
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
                    id: this.titilevalue,
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
            pushquestion () { // 移出试卷
                const that = this
                this.$bkInfo({
                    title: '确认要移出？',
                    confirmFn () {
                        that.moveout()
                    }
                })
            },
            moveout () { // 将题目移出卷子
                const flag = { value: 0 }
                for (const j in this.Selections) {
                    flag.value = 0
                    for (const i in this.papertree[0].children) {
                        for (const t in this.papertree[0].children[i].children) {
                            if (this.papertree[0].children[i].children[t].id === this.Selections[j].QuestionId) {
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
            tableRowClassName ({ row, rowIndex }) {
                if (row.status === '已录入') {
                    return 'success-row'
                }
            },
            addtitle () {
                this.$refs.appendSection.validate().then(validator => {
                    this.savetitle()
                }, validator => {
                    this.$bkMessage({
                        message: '输入有误',
                        theme: 'warning'
                    })
                })
            },
            savepaper () { // 保存试卷
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
            async savetitle () {
                const data = {
                    course_id: this.CourseId,
                    custom_type_info: [
                        {
                            custom_type_name: this.append.questiontitle
                        }
                    ]
                }
                this.$http.post('/course/question_title/', data).then(res => {
                    if (res.result === true) {
                        this.$bkMessage({
                            message: '添加成功',
                            theme: 'success'
                        })
                        this.$http.get('/course/question_title/', { params: { course_id: this.CourseId } }).then(res => {
                            if (res.result === true) {
                                this.paperquestiontype = []
                                for (const i in res.data.custom_types) {
                                    this.$set(this.paperquestiontypeMap, res.data.custom_types[i].custom_type_name, res.data.custom_types[i].id)
                                    this.paperquestiontype.push({
                                        name: res.data.custom_types[i].custom_type_name,
                                        id: res.data.custom_types[i].id
                                    })
                                }
                            }
                        })
                    }
                })
            },
            async getquestiontitle () { // 获得大题名字
                this.$http.get('/course/question_title/', { params: { course_id: this.CourseId } }).then(res => {
                    if (res.result === true) {
                        this.paperquestiontype = []
                        for (const i in res.data.custom_types) {
                            this.$set(this.paperquestiontypeMap, res.data.custom_types[i].custom_type_name, res.data.custom_types[i].id)
                            this.paperquestiontype.push({
                                name: res.data.custom_types[i].custom_type_name,
                                id: res.data.custom_types[i].id
                            })
                        }
                    }
                }).then(res => {
                    this.getpaperinfo()
                })
            },
            async getpaperinfo () { // 获得试卷信息
                this.$http.get('/course/manage_paper_question_contact/', { params: { paper_id: this.$route.query.paperid } }).then(res => {
                    if (res.result === true) {
                        const count = { val: 0 }
                        this.existlist = []
                        this.papertree[0].id = this.$route.query.paperid
                        for (const i in res.data) {
                            const tmp = []
                            for (const j in res.data[i]) {
                                this.$set(this.existlist, count.val++, res.data[i][j].question_id)
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
                    this.getquetionlist() // 获得题目
                })
            },
            async updatepaper (data) { // 保存试卷请求
                this.$http.post('/course/manage_paper_question_contact/', { paper_id: this.$route.query.paperid, paper_info: data }).then(res => {
                    if (res.result === true) {
                        this.$bkMessage({
                            message: res.message,
                            theme: 'success'
                        })
                    } else {
                        this.$bkMessage({
                            message: res.message,
                            theme: 'error'
                        })
                    }
                })
            }
        }

    }
</script>

<style>
.right {
    float: left;
    width:500px;
    padding-left:25px;
}
.left {
    float: left;
}
tr.bk-table-row.success-row {
    background-color: #E1ECFF;
}
.add-button {
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
.delete-button {
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
.monitor-navigation-content {
    overflow-y: scroll;
}
.type-select {
    display: inline-block;
    width: 200px;
    margin-top: 0px;
}
.bk-select .bk-select-name {
    display: inline-block;
    line-height: 32px;
    height: 22px;
}
.bk-select {
    line-height: 32px;
}
.radio-common {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    box-shadow: none;
}
</style>
