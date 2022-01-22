<template>
    <div class="yy-descriptions">
        <div class="header">
            <span class="title">{{ title }}</span>
            <span class="right">
                <slot name="hander"></slot>
            </span>
        </div>
        <bk-container :gutter="0">
            <bk-row>
                <bk-col :span="span" v-for="item in formConfig" :key="item.field">
                    <div class="yy-descriptions-item">
                        <div class="yy-descriptions-item-label yy-border">
                            {{ item.label }}
                        </div>
                        <div class="yy-descriptions-item-text yy-border" v-if="!isEdit">
                            {{ userInfo[item.field] }}
                        </div>
                        <div class="yy-descriptions-item-text yy-border" v-else>
                            <bk-input
                                :disabled="item.disabled"
                                v-model="userInfo[item.field]"
                            ></bk-input>
                        </div>
                    </div>
                </bk-col>
            </bk-row>
        </bk-container>
    </div>
</template>

<script>
    export default {
        props: {
            span: {
                type: Number,
                default: 6
            },
            title: {
                type: String,
                default: '标题'
            },
            isEdit: {
                type: Boolean,
                default: false
            },
            // 表单配置
            formConfig: {
                type: Array,
                default: () => []
            }
        },
        data () {
            return {
                userInfo: {
                }
            }
        },

        watch: {
            isEdit (newValue) {
                if (newValue === false) {
                    this.changeUserInfoResult()
                }
            }
        },
        created () {
            // 调用api请求
            this.getUserInfoResult()
        },
        methods: {
            // 请求事件
            async getUserInfoResult () {
                const url = '/account/get_user_info/'
                const res = await this.$http.get(url)
                this.userInfo = res.data
                if (this.userInfo['identity'] === 'TEACHER') {
                    this.userInfo['identity'] = '老师'
                }
                if (this.userInfo['identity'] === 'STUDENT') {
                    this.userInfo['identity'] = '学生'
                }
                if (this.userInfo['identity'] === 'NOT_CERTIFIED') {
                    this.userInfo['identity'] = '未认证'
                }
            },
            // post修改事件
            async changeUserInfoResult () {
                await this.$http.post('/course/update_user_info/', this.userInfo)
                await this.getUserInfoResult()
            }
        }
    }
</script>

<style scoped>
.bk-grid-col {
  margin-bottom: 0;
}
.header {
  display: flex;
  align-items: center;
}

.header .title {
  font-weight: 700;
  font-size: 26px;
  padding: 10px 20px;
}

.yy-border {
  border: 1px #d9ecff solid;
}
.yy-descriptions {
  margin: 20px;
}
.yy-descriptions-item {
  display: flex;
}
.yy-descriptions-item-label {
  flex: 1 !important;
  background-color: #ecf5ff;
  font-weight: 700;
  height: 44px;
  padding: 10px;
  margin: 0px -1px -1px 0px;
}

 .bk-form-input {
  border: none;
  padding: 0 !important;
  font-size: 16px;
  line-height: 38px;
}
.yy-descriptions-item-text {
  flex: 2;
  padding-left: 10px;
  line-height: 42px;
  margin: 0px -1px -1px 0px;
}
</style>
