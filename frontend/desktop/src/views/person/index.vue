<template>
    <div class="personal">
        <!-- ------------------ -->
        <YyDescriptions ref="info" title="个人中心" :form-config="infoConfig" :span="6" @Identified="identified = true">
            <div slot="hander">
                <bk-button theme="primary" size="small" @click="identify">
                    {{identityStatus}}
                </bk-button>
            </div>
        </YyDescriptions>
        <bk-dialog
            theme="primary"
            header-position="left"
            title="学分制主页认证"
            v-model="isShowDialog"
            @confirm="formConfirm"
        >
            <bk-form :label-width="80" :model="formData">
                <bk-form-item label="用户名" :required="true" :property="'username'">
                    <bk-input
                        v-model="formData.username"
                        placeholder="输入学分制主页账号"
                    ></bk-input>
                </bk-form-item>
                <bk-form-item label="密码" :required="true" :property="'password'">
                    <bk-input
                        type="password"
                        v-model="formData.password"
                        placeholder="输入学分制主页密码"
                    ></bk-input>
                </bk-form-item>
            </bk-form>
        </bk-dialog>
        <!-- -------------------- -->

        <YyDescriptions
            title="联系方式"
            :form-config="contactConfig"
            :is-edit="isEdit">
            <div slot="hander">
                <bk-button theme="primary" size="small" @click="isEdit = !isEdit">
                    {{ isEdit ? "确定" : "编辑" }}
                </bk-button>
            </div>
        </YyDescriptions>
    </div>
</template>

<script>
    import YyDescriptions from '../../components/yy-descriptions/index.js'

    import { infoConfig, contactConfig } from './config/index'

    export default {
        components: {
            YyDescriptions
        },
        data () {
            return {
                config: {
                    theme: 'info',
                    message: '',
                    offsetY: 80
                },
                identified: false,
                isShowDialog: false,
                isEdit: false,
                infoConfig: infoConfig,
                contactConfig: contactConfig,
                formData: {
                    username: '',
                    password: ''
                }
            }
        },
        computed: {
            identityStatus () {
                return this.identified ? '已认证' : '未认证'
            }
        },
        methods: {
            // 向后端发出的 网络请求 用axios实现的
            async formConfirm () {
                // console.log(this.formData)
                const res = await this.$http.post(
                    // 这段string 就是url地址
                    '/course/authenticate',
                    // 这段是提交的data
                    // JSON.stringify(this.formData)
                    this.formData
                )
                console.log(res)

                // 这个是刷新 就是重新获取 更新后的数据
                this.$refs.info.getUserInfoResult()
                
                if (res.result) {
                    this.config.theme = 'primary'
                    this.config.message = '认证成功'
                    this.$bkMessage(this.config)
                } else {
                    this.config.theme = 'error'
                    this.config.message = res.message
                    this.$bkMessage(this.config)
                }
            },
            identify () {
                if (this.identified) {
                    this.config.message = '用户已认证，如需取消认证请联系管理员'
                    this.$bkMessage(this.config)
                } else {
                    this.isShowDialog = true
                }
            }
        }
    }
</script>

<style scoped>
</style>
