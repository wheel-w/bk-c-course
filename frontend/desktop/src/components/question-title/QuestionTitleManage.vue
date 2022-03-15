<template>
    <div style="border-style:;display:inline-block">
        <bk-button :theme="'primary'" :title="'主要按钮'" icon="icon-block-shape" style="margin-left:5px;margin-bottom:21px;border-style:double;" @click="questionTitleManage">
            大题管理
        </bk-button>
        <bk-sideslider :is-show.sync="show" :quick-close="true" @hidden="handleHidden" @shown="handleShown">
            <div slot="header">大题管理</div>
            <div class="p20" slot="content">
                <bk-form :model="append" ref="appendChapter" :label-width="0">
                    <div class="appendChapter">
                        <bk-form-item :required="true" :rules="rules.questionTitle" :property="'appendText'" :icon-offset="135">
                            <bk-input ref="appendInput" :clearable="false" v-model="append.appendText" style="width:70%;" @blur="handleAppendBlur" @enter="appendChapter"></bk-input>
                            <bk-button :theme="'primary'" :title="'主要按钮'" class="mr10" @click="appendChapter" style="float:right;">
                                新增大题
                            </bk-button>
                        </bk-form-item>
                    </div>
                </bk-form>
                <div class="questionTitles">
                    <bk-table
                        :data="questionTitleList"
                        :size="size"
                        :outer-border="true"
                        :virtual-render="false"
                        :show-header="false"
                        @row-click="handleRowClick"
                        @row-dblclick="handleRowDbclick"
                        @selection-change="handleSelectChange"
                        height="480">
                        <bk-table-column
                            label="章节"
                            prop="custom_type_name"
                            sortable
                            width=""
                            @row-dblclick="handleRowDbclickChapter">
                            <template slot-scope="props">
                                <p v-if="!rowEditable(props.row.custom_type_id)">{{props.row.custom_type_name}}</p>
                                <bk-input
                                    ref="myinput"
                                    class="input1"
                                    v-model="props.row.custom_type_name"
                                    v-if="rowEditable(props.row.custom_type_id)"
                                    style=""
                                    @enter="handleEnter(props.row)"
                                    @blur="handleBlur(props.row)">
                                </bk-input>
                            </template>
                        </bk-table-column>
                    </bk-table>
                </div>
                <div class="saveChange">
                    <bk-button :theme="'primary'" :title="'主要按钮'" class="mr10" @click="saveChange">
                        保存
                    </bk-button>
                </div>
            </div>
        </bk-sideslider>
    </div>
</template>
<script>
    export default {
        name: 'QuestionTitleManage',
        props: {
            questiontitles: {
                type: Object,
                default: () => ({})
            }
        },
        data () {
            return {
                config: {
                    message: null,
                    theme: 'error',
                    offset: 80
                },
                rules: {
                    questionTitle: [
                        {
                            required: true,
                            message: '大题不能为空！',
                            trigger: 'change'
                        },
                        {
                            validator: (val) => {
                                const a = { val: 0 }
                                this.questionTitleList.forEach(element => {
                                    if (val === element.custom_type_name) {
                                        a.val = 1
                                        return false
                                    }
                                })
                                if (a.val === 0) {
                                    return true
                                }
                            },
                            message: '该大题已存在',
                            trigger: 'blur'
                        }
                    ]
                },
                show: false,
                editable: false,
                curRow: null,
                curQuestionTitle: null,
                changed: false,
                saved: false,
                append: {
                    appendText: null,
                    appendNumber: 0
                },
                selection: []
            }
        },
        computed: {
            questionTitleList () {
                return JSON.parse(JSON.stringify(this.questiontitles))
            }
        },
        watch: {
        },
        created () {
        },
        methods: {
            handleRowDbclick (row, event, column, rowIndex, columnIndex) {
                if (!row.custom_type_id) {
                    row.custom_type_id = 'focus'
                }
                this.curRow = row.custom_type_id
                this.curQuestionTitle = row.custom_type_name
                this.editable = !this.editable
                this.$nextTick(() => {
                    this.$refs.myinput.focus()
                })
            },
            handleEnter (row) {
                if (row.custom_type_id === 'focus') {
                    row.custom_type_id = null
                }
                this.editable = false
            },
            handleBlur (row) {
                if (row.custom_type_id === 'focus') {
                    row.custom_type_id = null
                }
                if (!row.custom_type_name || (this.repeated(this.questionTitleList, 'custom_type_name', row.custom_type_name) > 1)) {
                    row.custom_type_name = this.curQuestionTitle
                }
                this.editable = false
            },
            handleHidden () {
                this.editable = false
                this.$emit('updateQuestionTitle', this.questionTitleList, this.saved)
            },
            handleShown () {
            },
            rowEditable (questionTitleId) {
                return (questionTitleId === this.curRow && this.editable)
            },
            questionTitleManage () {
                this.show = true
            },
            saveChange () {
                this.saved = true
                if (this.changed) {
                    this.$emit('updateQuestionTitle', this.questionTitleList, this.saved)
                } else {
                    this.compare()
                    if (this.changed) {
                        this.$emit('updateQuestionTitle', this.questionTitleList, this.saved)
                    } else {
                        this.config.theme = 'warning'
                        this.config.message = '未做修改'
                        this.$bkMessage(this.config)
                    }
                }
                this.saved = false
                this.changed = false
            },
            appendChapter () {
                if (this.repeated(this.questionTitleList, 'custom_type_name', this.curQuestionTitle) > 0) {
                    this.$refs.appendChapter.validate().then(validator => {
                        this.questionTitleList.push({
                            custom_type_id: null,
                            custom_type_name: this.append.appendText
                        })
                        this.append.appendText = null
                        this.append.appendNumber = this.append.appendNumber + 1
                    }, validator => {
                        this.config.theme = 'error'
                        this.config.message = validator.content
                        this.$bkMessage(this.config)
                    })
                    this.$refs.appendInput.focus()
                    this.changed = true
                } else {
                    this.config.theme = 'warning'
                    this.config.message = '此大题已存在，不可重复添加'
                    this.$bkMessage(this.config)
                }
            },
            handleSelectChange (selection, row) {
                this.selection = selection
            },
            // deleteChapter (questionTitle) {
            //     if (questionTitle.custom_type_id === null || questionTitle.custom_type_id === 'focus') {
            //         this.append.appendNumber = this.append.appendNumber - 1
            //         if (this.append.appendNumber !== 0) {
            //             this.changed = true
            //         } else if (this.changed) {
            //             this.changed = false
            //         }
            //     } else {
            //         this.changed = true
            //     }
            //     this.questionTitleList.splice(this.questionTitleList.indexOf(questionTitle), 1)
            // },
            handleAppendBlur () {
                // this.$refs.appendChapter.clearRrror()
            },
            compare () {
                for (let i = 0; i < this.questionTitleList.length; i++) {
                    if (this.questionTitleList[i].custom_type_id !== this.questiontitles[i].custom_type_id || this.questionTitleList[i].custom_type_name !== this.questiontitles[i].custom_type_name) {
                        this.changed = true
                    }
                }
            },
            repeated (list, key, item) {
                let repeated = 0
                list.forEach(element => {
                    if (element[key] === item) {
                        repeated = repeated + 1
                    }
                })
                return repeated
            }
        }
    }
</script>
<style lang="postcss" scoped>
.appendChapter {
    margin-bottom: 10px;
}
.questionTitles {
    margin-bottom: 10px;
}
.deleteChapter {
    display: inline-block;
}
.saveChange {
    display: inline-block;
}
</style>
