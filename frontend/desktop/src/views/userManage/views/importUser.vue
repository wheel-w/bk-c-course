<template>
    <div id="importUser">
        <div class="topTab">
            <!-- 下拉框 -->
            <bk-select
                multiple
                enable-scroll-load
                prefix-icon="bk-icon icon-search"
                v-model="selectedUsers"
                :remote-method="handleSelectSearch"
                :scroll-loading="bottomLoadingOptions"
                searchable
                style="width: 400px"
                size="large"
                placeholder="点我选择导入用户"
            >
                <bk-option
                    v-for="option in batch.selectMap"
                    :key="option.username"
                    :id="option.username"
                    :name="option.username + '(' + option.display_name + ')'"
                    :disabled="option.disable"
                >
                </bk-option>
            </bk-select>
            <bk-button
                theme="primary"
                @click="tagConfig.visible = true"
                :disabled="batch.accountList.length === 0"
            >导入选中用户</bk-button
            >
        </div>
        <!-- 表格 -->
        <bk-table
            :data="batch.accountList"
            size="small"
            stripe
            height="60vh"
            @selection-change="handleSelect"
        >
            <!-- 表格空状态插槽 -->
            <template slot="empty">
                <!-- <bk-icon type="exclamation-triangle" /> -->
                <div style="font-weight: 800; font-size: 18px">请在上方搜索栏筛选</div>
            </template>
            <bk-table-column
                v-for="field in fields"
                :key="field.prop"
                :label="field.label"
                :prop="field.prop"
                :width="field.width"
            >
            </bk-table-column>
            <bk-table-column label="操作">
                <template slot-scope="props">
                    <!-- <bk-icon type="close-circle-shape" /> -->
                    <bk-button theme="primary" text @click="handleDeleteSingle(props.row)"
                    >删除</bk-button
                    >
                </template>
            </bk-table-column>
        </bk-table>
        <!-- 批量添加确认框，以及添加tag -->
        <bk-dialog
            v-model="tagConfig.visible"
            title="请选择导入用户身份"
            theme="primary"
            @confirm="handleImportAccounts"
            ok-text="确认导入"
        >
            <bk-radio-group v-model="tagConfig.tag_id">
                <bk-radio v-for="tag in tagConfig.tags" :key="tag.id" :value="tag.id">
                    <bk-tag
                        :style="'background-color:' + colorTransform(tag.tag_color)"
                    >{{ tag.tag_value }}</bk-tag
                    >
                </bk-radio>
            </bk-radio-group>
        </bk-dialog>
    </div>
</template>

<script>
    import { bkRadio } from 'bk-magic-vue'
    import { vueDebounce, colorTransform } from '@/common/util'
    /*
    搜索流程:
    1.提供关键字给后端，获得100条以内相关数据
    2.每一个被选中后，都会添加至表格中，且表格默认选中
    */
    export default {
        components: {
            bkRadio
        },
        data () {
            return {
                batch: {
                    // 下方表格中展示的账户信息
                    accountList: [],
                    // 下拉框渲染选项,
                    selectMap: []
                },
                tagConfig: {
                    visible: false,
                    tag_id: 1,
                    // 所有的tag
                    tags: [
                        {
                            tag_id: 1,
                            tag_value: '学生'
                        }
                    ]
                },
                // 后端返回的所有数据
                allAccounts: [],
                // 表格字段配置
                fields: [
                    {
                        label: '账户名',
                        prop: 'username',
                        width: '300'
                    },
                    {
                        label: '姓名',
                        prop: 'display_name',
                        width: '300'
                    },
                    {
                        label: '部门',
                        prop: 'departments',
                        width: '300'
                    }
                ],
                // 分页
                page: {
                    current: 1,
                    limit: 20,
                    count: 10,
                    limitList: [20]
                },
                // 关键字
                keyWord: ''
            }
        },
        computed: {
            // 下拉框已选择用户
            selectedUsers: {
                get () {
                    return this.batch.accountList.map((e) => e.username)
                },
                set (newVal) {
                    // 找出被选中的账号展示在表格里
                    this.batch.accountList = this.allAccounts.filter((x) => {
                        return newVal.indexOf(x.username) !== -1
                    })
                }
            }
        },
        mounted () {
            this.flushAccounts()
            this.getTags()
        },
        methods: {
            // 获取accout列表
            async getAccountlist () {
                await this.$http.get(`/api/accounts/?key=${this.keyWord}`).then((res) => {
                    if (res.data !== 'empty') {
                        this.allAccounts = res.data
                    } else {
                        this.allAccounts = []
                    }
                })
            },
            // 获取tag列表
            async getTags () {
                await this.$http
                    .get('/api/tags/?is_built_in=1')
                    .then((res) => (this.tagConfig.tags = res.data.results))
            },
            // 搜索
            flushAccounts () {
                this.getAccountlist().then(() => {
                    // account列表map成下拉框选项
                    this.batch.selectMap = this.allAccounts.map((item) => {
                        return {
                            username: item.username,
                            display_name: item.display_name,
                            disable: item.is_import
                        }
                    })
                })
            },
            // 传入account详细信息列表
            importUser (accountList) {
                // 本来想用map的，可是序列化还是要转成对象，索性直接用对象
                const form = {}
                form.username_name_map = {}
                accountList.map((x) => {
                    form.username_name_map[x.username] = x.display_name
                })
                form.tag_id = this.tagConfig.tag_id
                return this.$http.post(`/api/users/batch/add/`, form)
            },
            handleImportAccounts () {
                this.$bkInfo({
                    type: 'warning',
                    title: '确认导入所有选中用户？',
                    confirmLoading: true,
                    confirmFn: async () => {
                        try {
                            await new Promise((resolve, reject) => {
                                this.importUser(this.batch.accountList).then((res) => {
                                    if (res.code !== 0) {
                                        reject(res)
                                    }
                                    resolve()
                                })
                            })
                            this.$bkMessage({
                                message: '导入成功',
                                theme: 'success'
                            })
                            this.selectedUsers = []
                            return true
                        } catch (e) {
                            this.$bkMessage({ message: e.message, theme: 'error' })
                            return false
                        }
                    }
                })
            },
            // 从下方表格中删除条目
            handleDeleteSingle (row) {
                this.batch.accountList.forEach((item, i, arr) => {
                    if (item.username === row.username) {
                        arr.splice(i, 1)
                    }
                })
            },
            handleSelectSearch (keyWord) {
                this.keyWord = keyWord
                if (!keyWord) {
                    return
                }
                this.search()
            },
            search: vueDebounce('flushAccounts', 500),
            colorTransform
        }
    }
</script>

<style lang="postcss">
.topTab {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  margin-top: 5px;
  margin-bottom: 5px;
}
/* 选择标签居中 */
.bk-form-control {
  display: flex;
  justify-content: space-evenly;
}
</style>
