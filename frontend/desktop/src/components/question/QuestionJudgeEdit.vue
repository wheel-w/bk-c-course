<template>
    <div>
        <div class="question">
            <p>题目:</p>
            <bk-input
                type="textarea"
                :autosize="{ minRows: 2, maxRows: 2 }"
                placeholder="请输入题目内容"
                v-model="Question.question"
                style="width:84%;margin-left:1%;">
            </bk-input>
        </div>
        <div class="options">
            <bk-radio-group v-model="Question.answer">
                <div class="option" @click="chooseT">
                    <bk-radio name="T" value="true" style="margin-top: 38px;margin-left:10px;">
                        T
                    </bk-radio>
                </div>
                <div class="option" @click="chooseF">
                    <bk-radio name="F" value="false" style="margin-top: 38px;margin-left:10px;">
                        F
                    </bk-radio>
                </div>
            </bk-radio-group>
        </div>
        <p style="margin-left: 1%;">正确答案：{{Question.answer}}</p>
        <div class="analysis">
            <bk-switcher
                theme="primary"
                v-model="explainOpen"
                :show-text="true"
                on-text="解析"
                off-text="解析"
                @change="handleSwitcherChange">
            </bk-switcher>
            <bk-button theme="primary" @click="saveChange">保存修改</bk-button>
            <bk-input
                type="textarea"
                :autosize="{ minRows: 2, maxRows: 2 }"
                placeholder="请输入答案解析内容"
                v-model="Question.explain"
                v-if="explainOpen"
                style="width:84%;margin-left:1%;display:block;">
            </bk-input>
        </div>
        <div class="upload">
        </div>
    </div>
</template>
<script>
    export default {
        name: 'QuestionRadio',
        props: {
            info: {
                type: Object,
                default: () => ({})
            }
        },
        data () {
            return {
                saved: false,
                explainOpen: false,
                Question: JSON.parse(JSON.stringify(this.info))
            }
        },
        computed: {
        },
        created () {
            if (this.Question.explain) {
                this.explainOpen = true
            }
        },
        methods: {
            chooseT () {
                this.Question.answer = 'true'
            },
            chooseF () {
                this.Question.answer = 'false'
            },
            saveChange () {
                this.saved = true
                this.$emit('updateQuestion', this.Question)
                this.saved = false
            },
            handleSwitcherChange (status) {
                if (!status) {
                    this.Question.explain = null
                }
            }
        }
    }
</script>
<style lang="postcss" scoped>
.question {
    p {
        width:80%;
        margin-left:1%;
    }
}
.options {
    height: 140px;
    margin-left: 1%;
    margin-top: 10px;
    .option {
        border-color: ;
        border-style: solid;
        border-radius:10px;
        height:100px;
        width: 39%;
        margin-right: 80px;
        margin-bottom: 10px;
        display: inline-block;
    }
}
.analysis {
    .bk-switcher {
        margin-left: 10px;
    }
    .bk-button {
        margin-left: 71.5%;
        margin-bottom: 10px;
    }
}
.upload {
    margin-top: 10px;
    .bk-button {
        margin-left: 76%;
    }
}
</style>
