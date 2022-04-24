<template>
    <div id="importUser">
        <div class="topTab">
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
                    v-for="option in selectMap"
                    :key="option.username"
                    :id="option.username"
                    :name="option.display_name"
                >
                </bk-option>
            </bk-select>
            <bk-button theme="primary" @click="handleImportAccounts"
            >导入选中用户</bk-button
            >
        </div>
        <bk-table
            :data="accountList"
            size="small"
            stripe
            height="60vh"
            @selection-change="handleSelect"
        >
            <!-- 空状态 -->
            <template slot="empty">
                <bk-icon type="exclamation-triangle" />
                <div>请在上方搜索栏筛选</div>
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
                    <bk-icon type="close-circle-shape" />
                    <bk-button theme="primary" text @click="handleDeleteSingle(props.row)"
                    >从待添加列表删除</bk-button
                    >
                </template>
            </bk-table-column>
        </bk-table>
    </div>
</template>

<script>
    import { bkSelect, bkOption } from 'bk-magic-vue'
    /*
    搜索流程:
    1.提供关键字给后端，获得100条以内相关数据
    2.每一个被选中后，都会添加至表格中，且表格默认选中
    */
    const BASE_UEL = 'api/accounts/'
    export default {
        components: {
            bkSelect,
            bkOption
        },
        data () {
            return {
                // 后端返回的所有数据
                allAccounts: [],
                // 下方表格中展示的账户信息
                accountList: [],
                // 下拉框渲染选项,
                selectMap: [],
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
                    return this.accountList.map((e) => e.username)
                },
                set (newVal) {
                    // 找出被选中的账号展示在表格里
                    this.accountList = this.allAccounts.filter((x) => {
                        return newVal.indexOf(x.username) !== -1
                    })
                }
            }
        },
        mounted () {
            this.flushAccounts(this.keyWord)
        },
        methods: {
            // 获取accout列表
            async getAccountlist (keyWord) {
                await this.$http.get(`${BASE_UEL}?key=${keyWord}`).then((res) => {
                    this.allAccounts = res.data
                })
            },
            // 搜索
            flushAccounts (keyWord) {
                this.getAccountlist(keyWord).then(() => {
                    // account列表map成下拉框选项
                    this.selectMap = this.allAccounts.map((item) => {
                        return { username: item.username, display_name: item.display_name }
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
                form.tag_id = 2
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
                                this.importUser(this.accountList).then((res) => {
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
                this.accountList.forEach((item, i, arr) => {
                    if (item.username === row.username) {
                        arr.splice(i, 1)
                    }
                })
            },
            handleSelectSearch (key) {
                // 减少请求次数
                if (key == null) {
                    return null
                }
                this.flushAccounts(key)
            }
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
</style>
