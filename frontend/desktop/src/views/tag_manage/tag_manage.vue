<template>
    <div id="tag_manage">
        <div class="tag_control">
            <bk-button
                @click="
                    editDialog.visible = true;
                    editDialog.form = {};
                "
                theme="primary"
            >新增标签</bk-button
            >
            <!-- 筛选 -->
            <div class="screen">
                <bk-icon type="sort" />
                <bk-select
                    placeholder="所属项目"
                    v-model="screen.project"
                    style="width: 100px"
                    ext-cls="select-custom"
                    ext-popover-cls="select-popover-custom"
                    :clearable="false"
                    @selected="handleScreen"
                >
                    <bk-option
                        v-for="option in projectList"
                        :key="option.id"
                        :id="option.id"
                        :name="option.name"
                    >
                    </bk-option>
                </bk-select>
                <bk-select
                    placeholder="标签类型"
                    v-model="screen.is_built_in"
                    style="width: 100px"
                    ext-cls="select-custom"
                    ext-popover-cls="select-popover-custom"
                    :clearable="false"
                    @selected="handleScreen"
                >
                    <bk-option :key="1" :id="1" name="系统标签"> </bk-option>
                    <bk-option :key="0" :id="0" name="用户标签"> </bk-option>
                </bk-select>
                <bk-input
                    left-icon="bk-icon icon-search"
                    placeholder="搜索标签"
                    v-model="screen.keyword"
                    @blur="getTagList()"
                    @keyup.enter.native="getTagList()"
                    style="width: 200px"
                >
                    <!-- <bk-input
                    left-icon="bk-icon icon-search"
                    placeholder="搜索用户"
                    @blur="get()"
                    @keyup.enter.native="getUserlist()"
                    style="width: 300px"
                > -->
                </bk-input>
                <bk-button @click="handleClearScreen">清除筛选条件</bk-button>
            </div>
        </div>
        <!-- 标签们 -->
        <div class="tag_group">
            <tag
                v-for="tag in tags"
                :key="tag.id"
                :tag="tag"
                @listChange="getTagList"
                @updateTag="handleEditTag"
            ></tag>
        </div>
        <!-- 增改标签 -->
        <bk-dialog
            v-model="editDialog.visible"
            @confirm="handleConfirm"
            title="编辑标签"
            :mask-close="false"
            width="400px"
        >
            <bk-form label-width="80" :model="editDialog.form">
                <bk-form-item label="标签名称" :required="true">
                    <bk-input v-model="editDialog.form.tag_value"></bk-input>
                </bk-form-item>
                <bk-form-item
                    label="所属项目"
                    :required="true"
                    v-if="!editDialog.form.id"
                >
                    <!-- <bk-input v-model="editDialog.form.sub_project"></bk-input> -->
                    <bk-select
                        v-model="editDialog.form.sub_project"
                        style="width: 250px"
                        ext-cls="select-custom"
                        ext-popover-cls="select-popover-custom"
                        searchable
                    >
                        <bk-option
                            v-for="option in projectList"
                            :key="option.id"
                            :id="option.id"
                            :name="option.name"
                        >
                        </bk-option>
                    </bk-select>
                </bk-form-item>
                <bk-form-item label="标签颜色" :required="true">
                    <bk-color-picker
                        v-model="editDialog.form.tag_color"
                    ></bk-color-picker>
                </bk-form-item>
            </bk-form>
        </bk-dialog>
    </div>
</template>

<script>
    const tag = () => import('./components/tag')
    export default {
        components: { tag },
        data () {
            const projectList = JSON.parse(sessionStorage.getItem('projects'))
            return {
                tags: [],
                editDialog: {
                    visible: false,
                    form: {}
                },
                projectList,
                screen: {
                    project: '',
                    is_built_in: ''
                }
            }
        },
        mounted () {
            this.getTagList()
        },
        methods: {
            getTagList () {
                return this.$http
                    .get('/api/tags/', {
                        params: {
                            sub_project: this.screen.project,
                            is_built_in: this.screen.is_built_in,
                            tagvalue: this.screen.keyword
                        }
                    })
                    .then((res) => {
                        if (res.code === 0) {
                            // 有些标签的所属项目id根本不存在
                            // res.data.map(
                            //     (e) =>
                            //         (e.projectName = this.projectList.find((i) => (i.id === e.sub_project)).name)
                            // )
                            this.tags = res.data
                        }
                    })
            },
            addTag () {
                return new Promise((resolve, reject) => {
                    this.$http
                        .post('/api/tags/', {
                            tag_value: this.editDialog.form.tag_value,
                            tag_color: this.editDialog.form.tag_color.slice(-6),
                            sub_project: this.editDialog.form.sub_project
                        })
                        .then((res) => {
                            this.$bkMessage({
                                message: res.message,
                                theme: res.code === 0 ? 'success' : 'error'
                            })
                            this.editDialog.form = {}
                            this.getTagList()
                        })
                })
            },
            updateTag (id) {
                return this.$http
                    .put(`/api/tags/${id}/`, {
                        tag_value: this.editDialog.form.tag_value,
                        tag_color: this.editDialog.form.tag_color.slice(-6)
                    })
                    .then((res) => {
                        this.$bkMessage({
                            message: res.message,
                            theme: res.code === 0 ? 'success' : 'error'
                        })
                        this.editDialog.form = {}
                        this.getTagList()
                    })
            },
            handleConfirm () {
                if (
                    !this.editDialog.form.tag_color
                    || !this.editDialog.form.sub_project
                    || !this.editDialog.form.tag_value
                ) {
                    alert('请完整填写')
                    return null
                }

                switch (typeof this.editDialog.form.id) {
                    case 'number': // 修改
                        this.updateTag(this.editDialog.form.id)
                        break
                    case 'undefined': // 新增
                        this.addTag()
                        break
                }
            },
            handleEditTag (tag) {
                this.editDialog.form = tag
                this.editDialog.visible = true
            },
            handleScreen () {
                console.log(this.screen)
                this.getTagList()
            },
            handleClearScreen () {
                this.screen = {}
                this.getTagList()
            }
        }
    }
</script>

<style lang="postcss">
.tag_control {
  display: flex;
  background-color: rgb(194, 243, 232);
  .screen {
    display: flex;
    width: 100%;
    justify-content: flex-end;
    margin-left: 200px;
    background-color: #fff;

    & > div,
    & > button {
      width: 150px;
      margin-right: 15px;
    }
    .bk-icon.icon-sort:before {
      font-size: 26px;
      line-height: 30px;
    }
  }
  button {
    width: 200px;
  }
}
/* dot-menu */
.tag_menu {
  width: fit-content;
  float: right;
}
.tag_group {
  min-width: 1000px;
  display: grid;
  grid-template-columns: repeat(6, 16%);
  grid-template-rows: 130px;
  /* 兼容ie */
  * {
    align-self: center;
  }
}
</style>
