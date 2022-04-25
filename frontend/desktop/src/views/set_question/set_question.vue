<template>
    <div class="wrapper">
        <div class="navTab">
            <bk-tab :active.sync="active" type="unborder-card">
                <bk-tab-panel
                    v-for="(panel, index) in panels"
                    v-bind="panel"
                    :key="index">
                    <ul v-if="panel.name === 'questionType'">
                        <li>
                            <bk-button theme="default" size="small"
                                title="新增" @click="addSingle" class="mr10 questionType">单选题
                            </bk-button>
                        </li>
                        <li>
                            <bk-button theme="default" size="small"
                                title="新增" @click="addMulti" class="mr10 questionType">多选题
                            </bk-button>
                        </li>
                        <li>
                            <bk-button theme="default" size="small"
                                title="新增" @click="addJudge" class="mr10 questionType">判断题
                            </bk-button>
                        </li>
                        <li>
                            <bk-button theme="default" size="small"
                                title="新增" @click="addShort" class="mr10 questionType">简答题
                            </bk-button>
                        </li>
                    </ul>
                    <div v-if="panel.name === 'outline'">
                        此处生成题目大纲
                    </div>
                </bk-tab-panel>
            </bk-tab>
        </div>
        <div class="questionList">
            <ul :virtual-render="true" id="questionUl">
            </ul>
            <bk-button style="margin-top: 5px; margin-left: 45%; background-color: #88a2ef; color: #f6f6f6" @click="addQuestion.primary.visible = true">插入问题</bk-button>
        </div>
        <!--添加题型Dialog-->
        <bk-dialog v-model="addQuestion.primary.visible"
            theme="primary"
            :mask-close="false"
            :scrollable="true"
            :header-position="addQuestion.primary.headerPosition"
            title="请选择你要添加的题型">
            <bk-button theme="default" size="small"
                title="新增" @click="addSingle" class="mr10 questionType">单选题
            </bk-button>
            <bk-button theme="default" size="small"
                title="新增" @click="addMulti" class="mr10 questionType">多选题
            </bk-button>
            <bk-button theme="default" size="small"
                title="新增" @click="addJudge" class="mr10 questionType">判断题
            </bk-button>
            <bk-button theme="default" size="small"
                title="新增" @click="addShort" class="mr10 questionType">简答题
            </bk-button>
        </bk-dialog>
    </div>
</template>
<script>
    import singleSelection from '../../components/questionCard/singleSelection.vue'
    import multiSelection from '../../components/questionCard/multiSelection.vue'
    import shortAnswer from '../../components/questionCard/shortAnswer.vue'
    import judge from '../../components/questionCard/judge.vue'
    import Vue from 'vue'

    export default {
        components: {},
        data () {
            return {
                panels: [
                    { name: 'questionType', label: '常用题型', count: 10 },
                    { name: 'outline', label: '大纲', count: 20 }
                ],
                active: 'mission',
                customSettings: {
                    isShow: false,
                    title: '添加问题'
                },
                addQuestion: {
                    primary: {
                        visible: false,
                        headerPosition: 'left'
                    }
                }

            }
        },
        methods: {
            addSingle () {
                const liNode = document.createElement('li')
                liNode.setAttribute('id', 'single')
                const ulNode = document.querySelector('#questionUl')
                ulNode.appendChild(liNode)
                console.log('ul', ulNode)
                const Profile = Vue.extend(singleSelection)
                new Profile().$mount('#single')
            },
            addMulti () {
                const liNode = document.createElement('li')
                liNode.setAttribute('id', 'single')
                const ulNode = document.querySelector('#questionUl')
                ulNode.appendChild(liNode)
                console.log('ul', ulNode)
                const Profile = Vue.extend(multiSelection)
                new Profile().$mount('#single')
            },
            addShort () {
                const liNode = document.createElement('li')
                liNode.setAttribute('id', 'single')
                const ulNode = document.querySelector('#questionUl')
                ulNode.appendChild(liNode)
                console.log('ul', ulNode)
                const Profile = Vue.extend(shortAnswer)
                new Profile().$mount('#single')
            },
            addJudge () {
                const liNode = document.createElement('li')
                liNode.setAttribute('id', 'single')
                const ulNode = document.querySelector('#questionUl')
                ulNode.appendChild(liNode)
                console.log('ul', ulNode)
                const Profile = Vue.extend(judge)
                new Profile().$mount('#single')
            }
        }
    }
</script>
<style scoped>
    .navTab {
        width: 20%;
        height: 90%;
    }

    .navTab ul li {
        margin: 20px;
    }

    .questionList {
        position: relative;
        width: 78%;
        left: 21%;
        top: -91%;
        height: 100%;
        /*background-color: #f3f5f7;*/

    }

    .bk-form-item .bk-button {
        margin-top: 20px;
    }
    .questionType{
        color: #888888;
        border-radius: 3px;
        background-color: #f3f5f7;
    }
    .questionType:hover{
        background: #dfe1e3;
    }
    .questionType:active{
        border: #888;
        color: #1f1f1f;
    }
    .questionList #questionUl {
        height: 93%;
        width: 47%;
        margin: 0 auto;
        /*float: left;*/
        /*position: absolute;*/
        right: 1%;
        overflow: auto;
        margin-top: 2%;
    }

    .questionList ul {
        height: 100%;
        width: 100%;
        /*float: left;*/
        /*position: absolute;*/
        right: 1%;
        overflow: auto;
        margin-top: 2%;
    }

    .questionList #questionUl .singleSelection {
        margin-top: 1%;
        margin-bottom: 1%;
    }
</style>
