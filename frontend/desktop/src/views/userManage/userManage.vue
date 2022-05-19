<template>
    <div id="userManage">
        <bk-tab :active.sync="active" type="unborder-card">
            <!-- 为了保持数据同步，使用v-if销毁组件 -->
            <bk-tab-panel v-bind="{ name: 'userlist', label: '用户列表' }">
                <user-list v-if="active === 'userlist'"></user-list>
            </bk-tab-panel>
            <bk-tab-panel v-bind="{ name: 'accounts', label: '导入用户' }">
                <import-user v-if="active === 'accounts'"></import-user>
            </bk-tab-panel>
        </bk-tab>
    </div>
</template>

<script>
    import { bkTab, bkTabPanel } from 'bk-magic-vue'
    const userList = () => import('./views/userList')
    const importUser = () => import('./views/importUser')
    export default {
        components: {
            bkTab,
            bkTabPanel,
            userList,
            importUser
        },
        data () {
            return {
                active: 'userlist'
            }
        },
        mounted () {}
    }
</script>

<style lang="postcss">
.bk-tab-section {
  padding-top: 5px;
}
</style>
