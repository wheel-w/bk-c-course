<template>
    <div id="tag_manage">
        <div class="tag_control">
            <bk-button @click="editDialog.visible = true" theme="primary"
            >新增标签</bk-button
            >
        </div>
        <!-- 标签们 -->
        <div class="tag_group">
            <tag v-for="tag in tags" :key="tag" :tag="tag" @change="getTagList"></tag>
        </div>
        <!-- 增改标签 -->
        <bk-dialog
            v-model="editDialog.visible"
            @confirm="handleAddTag"
            title="编辑标签"
            :mask-close="false"
            width="400px"
        >
            <bk-form label-width="80" :model="editDialog.form">
                <bk-form-item label="标签名称" :required="true">
                    <bk-input v-model="editDialog.form.tag_value"></bk-input>
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
            return {
                tags: [],
                editDialog: {
                    visible: false,
                    form: {}
                }
            }
        },
        mounted () {
            this.getTagList()
            // this.addTag()
            // this.delTag()
        },
        methods: {
            getTagList () {
                return this.$http.get('/api/tags/').then((res) => {
                    this.tags = res.data
                })
            },
            addTag () {
                return this.$http
                    .post('/api/tags/', {
                        tag_value: this.editDialog.form.tag_value,
                        tag_color: this.editDialog.form.tag_color.slice(1),
                        sub_project: 1
                    })
                    .then(() => {
                        this.getTagList()
                    })
            },
            handleAddTag () {
                console.log(this.editDialog)
                this.addTag()
            },
            test () {
                console.log(arguments)
            }
        }
    }
</script>

<style lang="postcss">
.tag_control {
  background-color: rgb(194, 243, 232);
}
.tag_menu {
  width: fit-content;
  float: right;
}
.tag_group {
  display: grid;
  grid-template-columns: repeat(5, 20%);
  grid-template-rows: 160px;
  margin-top: 20px;
}
</style>
