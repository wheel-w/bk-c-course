<template>
    <div>
        <bk-dialog v-model="viewQrCode.primary.visible"
            theme="primary"
            ok-text="下载图片"
            cancel-text="关闭"
            :mask-close="false"
            :confirm-fn="saveQrCode"
            :header-position="viewQrCode.primary.headerPosition"
            @cancel="$refs.qrCodeUrl.innerHTML = ''">
            <div id="qrCodeBox" class="qrCodeBox">
                <div class="qrcode" id="qrCode" ref="qrCodeUrl"></div><br>
                <bk-tag theme="info">请扫描上方二维码答题</bk-tag>
            </div>
        </bk-dialog>
        <bk-dialog v-model="dialogsetting.custom.visible"
            width="720"
            ok-text="开始选题"
            @confirm="check"
            :auto-close="false"
            :position="dialogsetting.custom.position"
            @cancel="$refs.addform.clearError(), formData.start = undefined, formData.end = undefined"
            title="新增试卷">
            <bk-form ref="addform" :model="formData" :rules="rules1" label-width="200">
                <bk-form-item :required="true" :error-display-type="'normal'" :property="'papertype'" label="卷子类型:">
                    <bk-radio-group v-model="formData.papertype">
                        <bk-radio :value="'EXAM'">测试卷</bk-radio>
                        <bk-radio :value="'EXERCISE'">练习卷</bk-radio>
                    </bk-radio-group>
                </bk-form-item>
                <bk-form-item :required="true" :error-display-type="'normal'" :property="'papername'" style="width:460px" label="卷子名称:">
                    <bk-input v-model="formData.papername"></bk-input>
                </bk-form-item>
                <bk-form-item :required="true" :error-display-type="'normal'" :property="'chapter'" style="width:460px" label="所属章节:">
                    <bk-select v-model="formData.chapter" searchable>
                        <bk-option v-for="option in chapterlist"
                            :key="option.name"
                            :id="option.id"
                            :name="option.name">
                        </bk-option>
                    </bk-select>
                </bk-form-item>
                <bk-form-item :required="true" :error-display-type="'normal'" :property="'start'" label="开始时间:">
                    <bk-date-picker v-model="formData.start" :time-picker-options="timePickerOptions" :type="'datetime'"></bk-date-picker>
                </bk-form-item>
                <bk-form-item :required="true" :error-display-type="'normal'" :property="'end'" label="结束时间:">
                    <bk-date-picker v-model="formData.end" :time-picker-options="timePickerOptions" :type="'datetime'"></bk-date-picker>
                </bk-form-item>
            </bk-form>
        </bk-dialog>
        <bk-dialog v-model="editdialog.custom.visible"
            width="720"
            :position="editdialog.custom.position"
            ok-text="保存"
            :auto-close="false"
            @confirm="validatedata"
            @cancel="edit = true, $refs.paperinfo.clearError(), selectdata.start = undefined, selectdata.end = undefined"
            title="修改试卷信息">
            <bk-form label-width="200" :model="selectdata" :rules="rules" ref="paperinfo">
                <bk-form-item :error-display-type="'normal'" label="卷子类型:" :required="true" :property="'papertype'">
                    <bk-radio-group v-model="selectdata.papertype">
                        <bk-radio :disabled="edit" :value="'EXERCISE'">练习卷</bk-radio>
                        <bk-radio :disabled="edit" :value="'EXAM'">测试卷</bk-radio>
                    </bk-radio-group>
                </bk-form-item>
                <bk-form-item :error-display-type="'normal'" style="width:460px" label="卷子名称:" :required="true" :property="'papername'">
                    <bk-input
                        :readonly="edit"
                        v-model="selectdata.papername"></bk-input>
                </bk-form-item>
                <bk-form-item :error-display-type="'normal'" style="width:460px" label="所属章节:" :property="'paperchapterid'">
                    <bk-select v-model="selectdata.paperchapterid" searchable :readonly="edit">
                        <bk-option v-for="option in chapterlist"
                            :key="option.id"
                            :id="option.id"
                            :name="option.name">
                        </bk-option>
                    </bk-select>
                </bk-form-item>
                <bk-form-item :required="true" :error-display-type="'normal'" :property="'start'" label="开始时间:">
                    <bk-date-picker :clearable="!edit" :readonly="edit" v-model="selectdata.start" :time-picker-options="timePickerOptions" :type="'datetime'"></bk-date-picker>
                </bk-form-item>
                <bk-form-item :required="true" :error-display-type="'normal'" :property="'end'" label="结束时间:">
                    <bk-date-picker :clearable="!edit" :readonly="edit" v-model="selectdata.end" :time-picker-options="timePickerOptions" :type="'datetime'"></bk-date-picker>
                </bk-form-item>
                <bk-form-item>
                    <bk-button v-if="edit" @click="edit = false" theme="primary">编辑</bk-button>
                </bk-form-item>
            </bk-form>
        </bk-dialog>
        <bk-button @click="dialogsetting.custom.visible = true" theme="primary">新增试卷</bk-button>
        <bk-table style="margin-top: 15px;"
            ref="table"
            max-height="500px"
            :data="paperlist"
            :virtual-render="true"
            :pagination="pagination">
            <bk-table-column align="center" label="试卷名" prop="papername"></bk-table-column>
            <bk-table-column
                :filters="typeFilters"
                :filter-method="typeFilterMethod"
                align="center"
                label="类型"
                width="75"
                prop="papertype"></bk-table-column>
            <bk-table-column
                align="center"
                :filters="chapterFilters"
                :filter-method="chapterFilterMethod"
                label="所属章节"
                prop="paperchapter"></bk-table-column>
            <bk-table-column
                align="center"
                :filters="statusFilters"
                :filter-method="statusFilterMethod"
                label="状态"
                width="75"
                prop="paperstatus"></bk-table-column>
            <bk-table-column
                align="center"
                label="开始时间"
                prop="starttime"></bk-table-column>
            <bk-table-column
                align="center"
                label="结束时间"
                prop="endtime"></bk-table-column>
            <bk-table-column
                align="center"
                label="提交人数/总人数"
                prop="rate"></bk-table-column>
            <bk-table-column align="center" label="操作" width="280">
                <template slot-scope="props">
                    <bk-button class="mr10" theme="primary" text v-if="props.row.paperstatus === '草稿'" @click="publishpaper(props.row)">发布</bk-button>
                    <bk-button class="mr10" theme="primary" text v-else :disabled="props.row.paperstatus === '已批阅'" @click="cancel(props.row)">取消</bk-button>
                    <bk-button class="mr10" theme="primary" text :disabled="props.row.paperstatus !== '草稿'" @click="modifiypaper(props.row)">选题</bk-button>
                    <bk-button class="mr10" theme="primary" text :disabled="props.row.paperstatus === '草稿'" @click="markpaper(props.row)">批改</bk-button>
                    <bk-button class="mr10" theme="primary" text v-if="props.row.paperstatus === '已批阅'" @click="cancleScore(props.row)">撤回成绩</bk-button>
                    <bk-button class="mr10" theme="primary" text v-else :disabled="props.row.paperstatus === '草稿'" @click="publishScore(props.row)">发布成绩</bk-button>
                    <bk-popover class="dot-menu" placement="bottom-left" theme="dot-menu light" trigger="click"
                        :arrow="false" offset="15" :distance="0">
                        <span class="dot-menu-trigger"></span>
                        <ul class="dot-menu-list" slot="content">
                            <li class="dot-menu-item">
                                <bk-button class="mr10" theme="primary" text @click="openedit(props.row)">修改</bk-button>
                            </li>
                            <li class="dot-menu-item">
                                <bk-button class="mr10" theme="primary" text :disabled="props.row.isend" @click="viewQrCode.primary.visible = true, code(props.row)">扫码</bk-button>
                            </li>
                        </ul>
                    </bk-popover>
                </template>
            </bk-table-column>
        </bk-table>
        <bk-dialog v-model="publishScoreControl.visible"
            width="400"
            :header-position="publishScoreControl.headerPosition"
            :position="publishScoreControl.position"
            :title="publishScoreControl.isPubilsh ? '发布成绩' : '撤回成绩'"
            @confirm="changePaperStatus">
            <span style="font-size: 17px">
                {{ publishScoreControl.isPubilsh ? '您确定要发布成绩吗？' : '您确定要撤回成绩吗？' }}
            </span>
        </bk-dialog>
    </div>
</template>

<script>
    import QRCode from 'qrcodejs2'
    export default {
        data () {
            return {
                publishScoreControl: {
                    isPubilsh: true,
                    visible: false,
                    headerPosition: 'left',
                    position: {
                        top: 200
                    },
                    row: {}
                },
                viewQrCode: {
                    primary: {
                        visible: false,
                        headerPosition: 'left'
                    }
                },
                paperlist: [
                ],
                dialogsetting: {
                    custom: {
                        visible: false,
                        position: {
                            top: 100
                        }
                    }
                },
                editdialog: {
                    custom: {
                        visible: false,
                        position: {
                            top: 100
                        }
                    }
                },
                formData: {
                    papertype: undefined,
                    papername: undefined,
                    chapter: undefined,
                    start: undefined,
                    end: undefined
                },
                selectdata: {
                    papertype: undefined,
                    papername: undefined,
                    paperchapterid: undefined,
                    start: undefined,
                    end: undefined
                },
                edit: true,
                chapterlist: [
                ],
                chapterFilters: [
                ],
                statusFilters: [
                    {
                        text: '草稿',
                        value: '草稿'
                    },
                    {
                        text: '已发布',
                        value: '已发布'
                    },
                    {
                        text: '已批阅',
                        value: '已批阅'
                    }
                ],
                typeFilters: [
                    {
                        text: '测试卷',
                        value: '测试卷'
                    },
                    {
                        text: '练习卷',
                        value: '练习卷'
                    }
                ],
                selectpaper: undefined,
                rules1: {
                    papertype: [
                        {
                            required: true,
                            message: '必选项',
                            trigger: 'blur'
                        }
                    ],
                    papername: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        },
                        {
                            max: 15,
                            message: '不能多于15字符',
                            trigger: 'blur'
                        }
                    ],
                    chapter: [
                        {
                            required: true,
                            message: '必选项',
                            trigger: 'blur'
                        }
                    ],
                    start: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        },
                        {
                            validator: (val) => {
                                if (this.formData.end === undefined || this.formData.end === '') {
                                    return true
                                } else {
                                    if (val.getTime() < this.formData.end.getTime()) {
                                        return true
                                    } else {
                                        return false
                                    }
                                }
                            },
                            message: '开始时间应早于结束时间',
                            trigger: 'blur'
                        }
                    ],
                    end: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        },
                        {
                            validator: (val) => {
                                if (this.formData.start === undefined || this.formData.start === '') {
                                    return true
                                } else {
                                    if (this.formData.start.getTime() < val.getTime()) {
                                        return true
                                    } else {
                                        return false
                                    }
                                }
                            },
                            message: '结束时间应晚于开始时间',
                            trigger: 'blur'
                        }
                    ]
                },
                rules: {
                    papertype: [
                        {
                            required: true,
                            message: '必选项',
                            trigger: 'blur'
                        }
                    ],
                    papername: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        }
                    ],
                    paperchapterid: [
                        {
                            required: true,
                            message: '必选项',
                            trigger: 'blur'
                        }
                    ],
                    start: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        },
                        {
                            validator: (val) => {
                                if (this.selectdata.end === undefined || this.selectdata.end === '') {
                                    return true
                                } else {
                                    if (this.selectdata.start.getTime() < this.selectdata.end.getTime()) {
                                        return true
                                    } else {
                                        return false
                                    }
                                }
                            },
                            message: '开始时间应早于结束时间',
                            trigger: 'blur'
                        }
                    ],
                    end: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        },
                        {
                            validator: (val) => {
                                if (this.selectdata.start === undefined || this.selectdata.start === '') {
                                    return true
                                } else {
                                    if (this.selectdata.start.getTime() < this.selectdata.end.getTime()) {
                                        return true
                                    } else {
                                        return false
                                    }
                                }
                            },
                            message: '结束时间应晚于开始时间',
                            trigger: 'blur'
                        }
                    ]
                }
            }
        },
        computed: {
            CourseId: function () {
                return this.$store.state.currentCourseId
            }
        },
        watch: {
            CourseId: {
                handler () {
                    this.getchapterlist()
                }
            }
        },
        created () {
            this.getchapterlist()
        },
        methods: {
            // 撤回成绩
            cancleScore (row) {
                this.publishScoreControl.isPubilsh = false
                this.publishScoreControl.visible = true
                this.publishScoreControl.row = row
            },
            // 改变试卷状态
            async changePaperStatus () {
                if (this.publishScoreControl.isPubilsh) {
                    this.$http.get('/course/get_student_answer_info/', { params: { course_id: this.$store.state.currentCourseId, paper_id: this.publishScoreControl.row.id } }).then(res => {
                        let studentInfoList = []
                        studentInfoList = res.data.submitted.filter(item => {
                            return item.status === 'SUBMITTED' || item.status === 'MARKED' || item.status === 'SAVED'
                        })

                        // 为空时候代表卷子无需批改直接出成绩
                        if (studentInfoList.length === 0) {
                            this.$http.put('/course/paper/', { course_id: this.$store.state.currentCourseId, paper_id: this.publishScoreControl.row.id, update_info: { status: 'MARKED' } }).then(res => {
                                if (res.code === 200) {
                                    this.$bkMessage({
                                        message: '发布成功！',
                                        theme: 'success'
                                    })
                                    this.getpaperlist()
                                } else {
                                    this.$bkMessage({
                                        message: res.message,
                                        theme: 'warning'
                                    })
                                }
                            })
                        } else {
                            // 如果全部批改完毕更改paper状态
                            if (studentInfoList.every(item => {
                                return item.status === 'MARKED'
                            })) {
                                this.$http.put('/course/paper/', { course_id: this.$store.state.currentCourseId, paper_id: this.publishScoreControl.row.id, update_info: { status: 'MARKED' } }).then(res => {
                                    if (res.code === 200) {
                                        this.$bkMessage({
                                            message: '发布成功！',
                                            theme: 'success'
                                        })
                                        this.getpaperlist()
                                    } else {
                                        this.$bkMessage({
                                            message: res.message,
                                            theme: 'warning'
                                        })
                                    }
                                })
                            } else {
                                this.$bkMessage({
                                    message: '请批改完成所有试卷再提交哦！',
                                    theme: 'warning'
                                })
                            }
                        }
                    })
                } else {
                    this.$http.put('/course/paper/', { course_id: this.$store.state.currentCourseId, paper_id: this.publishScoreControl.row.id, update_info: { status: 'RELEASE' } }).then(res => {
                        if (res.code === 200) {
                            this.$bkMessage({
                                message: '撤回成功！',
                                theme: 'success'
                            })
                            this.getpaperlist()
                        } else {
                            this.$bkMessage({
                                message: res.message,
                                theme: 'warning'
                            })
                        }
                    })
                }
            },
            // 发布成绩
            publishScore (row) {
                if (new Date().getTime() > Date.parse(row.endtime)) {
                    this.publishScoreControl.isPubilsh = true
                    this.publishScoreControl.visible = true
                    this.publishScoreControl.row = row
                } else {
                    this.$bkMessage({
                        message: '请等待考试结束再发布成绩哦！',
                        theme: 'warning'
                    })
                }
            },
            utc2beijing (time) {
                // 计算出北京时间
                const date = new Date(time)
                const timestamp1 = date.getTime()
                const timestamp2 = timestamp1 / 1000
                const timestamp3 = timestamp2 + 8 * 60 * 60
                // 转换成UTC格式
                const tmp = new Date(parseInt(timestamp3) * 1000).toISOString()
                // 转化成 yyyy-mm-dd hh:mm
                const Tpos = tmp.indexOf('T')
                const Zpos = tmp.indexOf('Z')
                const yearmonthday = tmp.substr(0, Tpos)
                const hourminutesecond = tmp.substr(Tpos + 1, Zpos - Tpos - 8)
                const beijing = yearmonthday + ' ' + hourminutesecond
                return beijing
            },
            beijingtime (time) {
                const date = new Date(time)
                const timestamp1 = date.getTime()
                const timestamp2 = timestamp1 / 1000
                const timestamp3 = timestamp2 + 8 * 60 * 60
                // 转换成UTC格式
                const tmp = new Date(parseInt(timestamp3) * 1000).toISOString()
                return tmp
            },
            typeFilterMethod (value, row, column) { // 通过试卷类型过滤
                const property = column.property
                return row[property] === value
            },
            chapterFilterMethod (value, row, column) { // 通过题型过滤
                const property = column.property
                return row[property] === value
            },
            statusFilterMethod (value, row, column) { // 通过状态过滤
                const property = column.property
                return row[property] === value
            },
            async getchapterlist () { // 获得章节
                this.$http.get('/course/get_chapter_list/', { params: { course_id: this.CourseId } }).then(res => {
                    this.chapterFilters.splice(0, this.chapterFilters.length)
                    this.$set(this.chapterFilters, 0, {
                        text: '全部章节',
                        value: '全部章节'
                    })
                    this.chapterlist = [{ id: -1, name: '全部章节' }]
                    if (res.data.length !== 0) {
                        const count = { val: 1 }
                        for (const i in res.data) {
                            this.chapterlist.push({
                                id: res.data[i].id,
                                name: res.data[i].chapter_name
                            })
                            this.$set(this.chapterFilters, count.val++, {
                                text: res.data[i].chapter_name,
                                value: res.data[i].chapter_name
                            })
                        }
                    }
                }).then(res => {
                    this.getpaperlist() // 获得试卷
                })
            },
            getpaperlist () { // 获得试卷
                this.$http.get('/course/paper/', { params: { course_id: this.CourseId } }).then(res => {
                    this.paperlist = []
                    if (res.data.length !== 0) {
                        for (const i in res.data) {
                            const tmp = {
                                id: undefined,
                                papername: undefined,
                                paperchapter: undefined,
                                paperchapterid: undefined,
                                papertype: undefined,
                                types: undefined,
                                paperstatus: undefined,
                                starttime: undefined,
                                endtime: undefined,
                                start: undefined,
                                end: undefined,
                                submited: undefined,
                                sum: undefined,
                                rate: undefined,
                                isend: undefined
                            }
                            const now = new Date()
                            const end = new Date(res.data[i].end_time)
                            if (now.getTime() >= end.getTime()) {
                                tmp.isend = true
                            } else {
                                tmp.isend = false
                            }
                            tmp.papername = res.data[i].paper_name
                            tmp.id = res.data[i].id
                            tmp.paperchapterid = res.data[i].chapter_id
                            tmp.types = res.data[i].types
                            tmp.paperchapter = res.data[i].chapter_name
                            if (res.data[i].submitted_students_num !== undefined && res.data[i].total_students_num !== null) {
                                tmp.submited = res.data[i].submitted_students_num
                                tmp.sum = res.data[i].total_students_num
                                tmp.rate = res.data[i].submitted_students_num + '/' + res.data[i].total_students_num
                            } else {
                                tmp.rate = '———'
                            }
                            if (res.data[i].end_time !== null) {
                                tmp.endtime = this.utc2beijing(res.data[i].end_time)
                                tmp.end = this.beijingtime(res.data[i].end_time)
                            }
                            if (res.data[i].start_time !== null) {
                                tmp.start = this.beijingtime(res.data[i].start_time)
                                tmp.starttime = this.utc2beijing(res.data[i].start_time)
                            }
                            if (res.data[i].types === 'EXAM') {
                                tmp.papertype = '测试卷'
                            }
                            if (res.data[i].types === 'EXERCISE') {
                                tmp.papertype = '练习卷'
                            }
                            if (res.data[i].status === 'DRAFT') {
                                tmp.paperstatus = '草稿'
                            }
                            if (res.data[i].status === 'RELEASE') {
                                tmp.paperstatus = '已发布'
                            }
                            if (res.data[i].status === 'MARKED') {
                                tmp.paperstatus = '已批阅'
                            }
                            this.$set(this.paperlist, i, tmp)
                        }
                    }
                })
            },
            check () { // 创建试卷并跳转
                this.$refs.addform.validate().then(validator => {
                    this.dialogsetting.custom.visible = false
                    const data = {
                        course_id: this.CourseId,
                        types: this.formData.papertype,
                        chapter_id: this.formData.chapter,
                        paper_name: this.formData.papername
                    }
                    const timedate = {
                        start_time: this.formData.start,
                        end_time: this.formData.end
                    }
                    this.$http.post('/course/paper/', data).then(res => {
                        if (res.result === true) {
                            this.$http.put('/course/paper/', { course_id: this.CourseId, paper_id: res.data.paper_id, update_info: timedate }).then(res2 => {
                                if (res2.result === false) {
                                    this.$bkMessage({
                                        message: res2.message,
                                        theme: 'warning'
                                    })
                                }
                            })
                            if (data.chapter_id === -1) { // 全部章节不用传chapterid
                                this.$router.push({
                                    name: 'selectquestion',
                                    query: {
                                        paperid: res.data.paper_id
                                    }
                                })
                            } else {
                                this.$router.push({
                                    name: 'selectquestion',
                                    query: {
                                        chapterid: data.chapter_id,
                                        paperid: res.data.paper_id
                                    }
                                })
                            }
                        } else {
                            this.$bkMessage({
                                message: res.message,
                                theme: 'error'
                            })
                        }
                    })
                }, validator => {
                    this.dialogsetting.custom.visible = true
                    this.$bkMessage({
                        message: '请检查输入',
                        theme: 'warning'
                    })
                })
            },
            modifiypaper (row) {
                if (row.paperchapterid === -1) { // 全部章节不用传chapterid
                    this.$router.push({
                        name: 'selectquestion',
                        query: {
                            paperid: row.id
                        }
                    })
                } else {
                    this.$router.push({
                        name: 'selectquestion',
                        query: {
                            chapterid: row.paperchapterid,
                            paperid: row.id
                        }
                    })
                }
            },
            open (row) { // 打开发布对话框
                this.publishdialog.visible = true
                this.selectpaper = row.id
            },
            openedit (row) { // 打开修改试卷信息对话框
                this.editdialog.custom.visible = true
                this.selectdata.paperid = row.id
                this.selectdata.papername = row.papername
                this.selectdata.paperchapterid = row.paperchapterid
                this.selectdata.papertype = row.types
                this.selectdata.start = row.start
                this.selectdata.end = row.end
            },
            validatedata () {
                if (this.edit === false) {
                    this.$refs.paperinfo.validate().then(validator => {
                        const info = {
                            paper_name: this.selectdata.papername,
                            chapter_id: this.selectdata.paperchapterid,
                            types: this.selectdata.papertype,
                            start_time: this.selectdata.start,
                            end_time: this.selectdata.end
                        }
                        this.$http.put('/course/paper/', { course_id: this.CourseId, paper_id: this.selectdata.paperid, update_info: info }).then(res => {
                            if (res.result === true) {
                                this.$bkMessage({
                                    message: '保存成功',
                                    theme: 'success'
                                })
                                this.getpaperlist()
                                this.editdialog.custom.visible = false
                                this.selectdata.start = undefined
                                this.selectdata.end = undefined
                                this.edit = true
                            } else {
                                this.$bkMessage({
                                    message: res.message,
                                    theme: 'error'
                                })
                            }
                        })
                    }, validator => {
                        this.$bkMessage({
                            message: '请检查输入',
                            theme: 'warning'
                        })
                    })
                } else {
                    this.$bkMessage({
                        message: '保存成功',
                        theme: 'success'
                    })
                    this.editdialog.custom.visible = false
                }
            },
            cancel (row) {
                const that = this
                this.$bkInfo({
                    title: '确认取消发布？',
                    confirmFn () {
                        that.docancel(row.id)
                    }
                })
            },
            docancel (id) {
                const info = {
                    status: 'DRAFT'
                }
                this.$http.put('/course/paper/', { course_id: this.CourseId, paper_id: id, update_info: info }).then(res => {
                    if (res.result === true) {
                        this.$bkMessage({
                            message: '取消成功！',
                            theme: 'success'
                        })
                    } else {
                        this.$bkMessage({
                            message: res.message,
                            theme: 'error'
                        })
                    }
                }).then(res => {
                    this.getpaperlist()
                })
            },
            publishpaper (row) {
                const now = new Date()
                const end = new Date(row.end)
                if (now.getTime() >= end.getTime()) {
                    this.$bkMessage({
                        message: '结束时间设置不合理，发布失败',
                        theme: 'error'
                    })
                } else {
                    const info = {
                        status: 'RELEASE'
                    }
                    this.$http.put('/course/paper/', { course_id: this.CourseId, paper_id: row.id, update_info: info }).then(res => {
                        if (res.result === true) {
                            this.$bkMessage({
                                message: '发布成功！',
                                theme: 'success'
                            })
                        } else {
                            this.$bkMessage({
                                message: res.message,
                                theme: 'error'
                            })
                        }
                        this.getpaperlist()
                    })
                }
            },
            markpaper (row) { // 跳转批改试卷
                this.$router.push({
                    name: 'correct_paper',
                    query: {
                        paperid: row.id,
                        endTime: row.endtime
                    }
                })
            },
            code (row) {
                const now = new Date()
                const end = new Date(row.end)
                if (now.getTime() >= end.getTime()) {
                    this.$bkMessage({
                        message: '答卷时间已过',
                        theme: 'error'
                    })
                    this.getpaperlist()
                } else {
                    this.$nextTick(function () {
                        this.bindQRCode(row.id)
                    })
                }
            },
            bindQRCode (id) {
                // eslint-disable-next-line no-new
                new QRCode(this.$refs.qrCodeUrl, {
                    text: String(id),
                    width: 200,
                    height: 200,
                    colorDark: '#000000', // 二维码颜色
                    colorLight: '#ffffff', // 二维码背景色
                    correctLevel: QRCode.CorrectLevel.H// 容错率，L/M/H
                })
            },
            saveQrCode () {
                // 找到canvas标签
                const myCanvas = document.getElementById('qrCode').getElementsByTagName('canvas')
                // 创建一个a标签节点
                const a = document.createElement('a')
                // 设置a标签的href属性（将canvas变成png图片）
                a.href = myCanvas[0].toDataURL('image/png').replace('image/png', 'image/octet-stream')
                // 设置下载文件的名字
                a.download = '答题二维码.png'
                // 点击
                a.click()
            }
        }
    }
</script>

<style>
.time {
    display: inline-block;
    width: 125px
}
#qrCodeBox .bk-tag{
    position: absolute;
    left: 50%;
    margin-left: -70px;
}
#qrCodeBox{
    height: 280px;
    margin: 0 auto;
}
.qrCodeBox {
    width: 300px;
    height: 280px;
    position: relative;
    border: 1px solid #0b7ffe;
}

.qrCodeBox::before,
.qrCodeBox::after {
    content: "";
    position: absolute;
    width: 30px;
    height: 30px;
    animation: qrCodeBoxAni 1500ms infinite linear;
}

.qrCodeBox::before {
    top: -10px;
    left: -10px;
    border-top: 1px solid #0b7ffe;
    border-left: 1px solid #0b7ffe;
}

.qrCodeBox::after {
    right: -10px;
    bottom: -10px;
    border-bottom: 1px solid #0b7ffe;
    border-right: 1px solid #0b7ffe;
}

@keyframes qrCodeBoxAni{
    0% {
        width: 30px;
        height: 30px;
    }
    50% {
        width: calc(100% + 9px);
        height: calc(100% + 9px);
    }
    100% {
        width: 30px;
        height: 30px;
    }
}
.qrcode{
    width: 200px;
    height: 200px;
    margin: 0 auto;
    margin-top: 20px;
}
.qrcode img{
    margin: 0 auto;
}
.tag-view {
    margin-top: 20px;
    margin: 0 auto;
}

.dot-menu {
        display: inline-block;
        vertical-align: middle;
    }

    .tippy-tooltip.dot-menu-theme {
        padding: 0;
    }

    .dot-menu-trigger {
        display: block;
        width: 30px;
        height: 30px;
        line-height: 30px;
        border-radius: 50%;
        text-align: center;
        font-size: 0;
        cursor: pointer;
    }

    .dot-menu-trigger:hover {
        color: #3A84FF;
        background-color: #DCDEE5;
    }

    .dot-menu-trigger:before {
        content: "";
        display: inline-block;
        width: 3px;
        height: 3px;
        border-radius: 50%;
        background-color: currentColor;
        box-shadow: 0 -4px 0 currentColor, 0 4px 0 currentColor;
    }

    .dot-menu-list {
        margin: 0;
        padding: 5px 0;
        min-width: 50px;
        list-style: none;
    }

    .dot-menu-list .dot-menu-item {
        padding: 0 10px;
        font-size: 12px;
        line-height: 26px;
        cursor: pointer;

        &:hover {
            background-color: #eaf3ff;
            color: #3a84ff;
        }
    }
</style>
