<template>
    <div id="userConfig">
        <bk-dialog
            v-model="visible"
            :title="title"
            @after-leave="$emit('update:visible', visible)"
            @confirm="handleConfirm()"
            :position="{ top: 100 }"
            width="600px"
        >
            <bk-form :model="config">
                <bk-form-item label="username" required label-width="100">
                    <bk-input v-model="config.username"></bk-input>
                </bk-form-item>
                <bk-form-item label="name" required label-width="100">
                    <bk-input v-model="config.name"></bk-input>
                </bk-form-item>
                <bk-form-item label="性别" label-width="100">
                    <bk-radio-group v-model="config.gender">
                        <bk-radio value="MALE">男</bk-radio>
                        <bk-radio value="FEMALE">女</bk-radio>
                    </bk-radio-group>
                </bk-form-item>
                <bk-form-item label="邮箱" label-width="100">
                    <bk-input v-model="config.email"></bk-input>
                </bk-form-item>
                <bk-form-item label="QQ" label-width="100">
                    <bk-input v-model="config.qq_number"></bk-input>
                </bk-form-item>
            </bk-form>
        </bk-dialog>
    </div>
</template>

<script>
    export default {
        props: {
            title: {
                type: String,
                require: true
            },
            visible: {
                type: Boolean,
                require: true
            },
            config: {
                type: Object,
                default: {}
            }
        },
        data () {
            return {}
        },
        methods: {
            handleConfirm () {
                this.$http
                    .put(`api/user/update/${this.config.id}/`, { ...this.config })
                    .then(
                        (res) => {
                            console.log(res)
                            this.$bkMessage({
                                message: '修改成功',
                                theme: 'success'
                            })
                        }
                    )
            }
        }
    }
</script>
