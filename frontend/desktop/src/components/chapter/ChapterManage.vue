<template>
    <div style="border-style:;display:inline-block">
        <bk-button :theme="'primary'" :title="'主要按钮'" icon="icon-block-shape" style="margin-left:5px;margin-bottom:21px;border-style:double;" @click="chapterManage">
            章节管理
        </bk-button>
        <bk-sideslider :is-show.sync="show" :quick-close="true" @hidden="handleHidden" @shown="handleShown">
            <div slot="header">章节管理</div>
            <div class="p20" slot="content">
                <bk-form :model="append" ref="appendChapter" :label-width="0">
                    <div class="appendChapter">
                        <bk-form-item :required="true" :rules="rules.chapter" :property="'appendText'" :icon-offset="135">
                            <bk-input ref="appendInput" :clearable="false" v-model="append.appendText" style="width:70%;" @blur="handleAppendBlur" @enter="appendChapter"></bk-input>
                            <bk-button :theme="'primary'" :title="'主要按钮'" class="mr10" @click="appendChapter" style="float:right;">
                                新增章节
                            </bk-button>
                        </bk-form-item>
                    </div>
                </bk-form>
                <div class="chapters">
                    <bk-table
                        :data="chapterList"
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
                            prop="chapter_name"
                            sortable
                            width="250"
                            @row-dblclick="handleRowDbclickChapter">
                            <template slot-scope="props">
                                <p v-if="!rowEditable(props.row.id)">{{props.row.chapter_name}}</p>
                                <bk-input
                                    ref="myinput"
                                    class="input"
                                    v-model="props.row.chapter_name"
                                    v-if="rowEditable(props.row.id)"
                                    style="display:inline-block;"
                                    @enter="handleEnter(props.row)"
                                    @blur="handleBlur(props.row)">
                                </bk-input>
                            </template>
                        </bk-table-column>
                        <bk-table-column
                            label="操作"
                            align="right">
                            <template slot-scope="props">
                                <bk-button class="mr10" theme="default" icon="delete" :outline="true" size="small" @click="deleteChapter(props.row)"></bk-button>
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
        name: 'ChapterManage',
        props: {
            chapters: {
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
                    chapter: [
                        {
                            required: true,
                            message: '章节不能为空！',
                            trigger: 'change'
                        }
                    ]
                },
                show: false,
                editable: false,
                curRow: null,
                curChapter: null,
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
            chapterList () {
                return JSON.parse(JSON.stringify(this.chapters))
            }
        },
        watch: {
        },
        created () {
        },
        methods: {
            handleRowDbclick (row, event, column, rowIndex, columnIndex) {
                if (!row.id) {
                    row.id = 'focus'
                }
                this.curRow = row.id
                this.curChapter = row.chapter_name
                this.editable = !this.editable
                this.$nextTick(() => {
                    this.$refs.myinput.focus()
                })
            },
            handleEnter (row) {
                if (row.id === 'focus') {
                    row.id = null
                }
                if (row.chapter_name) {
                    this.editable = false
                } else {
                    row.chapter_name = this.curChapter
                    this.editable = false
                }
            },
            handleBlur (row) {
                if (row.id === 'focus') {
                    row.id = null
                }
                if (row.chapter_name) {
                    this.editable = false
                } else {
                    row.chapter_name = this.curChapter
                    this.editable = false
                }
            },
            handleHidden () {
                this.editable = false
                this.$emit('updateChapter', this.chapterList, this.saved)
            },
            handleShown () {
            },
            rowEditable (chapterId) {
                return (chapterId === this.curRow && this.editable)
            },
            chapterManage () {
                this.show = true
            },
            saveChange () {
                this.saved = true
                if (this.changed) {
                    this.$emit('updateChapter', this.chapterList, this.saved)
                } else {
                    this.compare()
                    if (this.changed) {
                        this.$emit('updateChapter', this.chapterList, this.saved)
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
                this.$refs.appendChapter.validate().then(validator => {
                    this.chapterList.push({
                        id: null,
                        chapter_name: this.append.appendText
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
            },
            handleSelectChange (selection, row) {
                this.selection = selection
            },
            deleteChapter (chapter) {
                if (chapter.id === null || chapter.id === 'focus') {
                    this.append.appendNumber = this.append.appendNumber - 1
                    if (this.append.appendNumber !== 0) {
                        this.changed = true
                    } else if (this.changed) {
                        this.changed = false
                    }
                } else {
                    this.changed = true
                }
                this.chapterList.splice(this.chapterList.indexOf(chapter), 1)
            },
            handleAppendBlur () {
                // this.$refs.appendChapter.clearRrror()
            },
            compare () {
                for (let i = 0; i < this.chapterList.length; i++) {
                    if (this.chapterList[i].id !== this.chapters[i].id || this.chapterList[i].chapter_name !== this.chapters[i].chapter_name) {
                        this.changed = true
                    }
                }
            }
        }
    }
</script>
<style lang="postcss" scoped>
.appendChapter {
    margin-bottom: 10px;
    .bk-button {
    }
}
.chapters {
    margin-bottom: 10px;
}
.deleteChapter {
    display: inline-block;
}
.saveChange {
    display: inline-block;
    margin-left:;
}
</style>
