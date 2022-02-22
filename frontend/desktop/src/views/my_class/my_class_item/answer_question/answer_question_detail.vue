<template>
    <div class="wrapper" v-if="$route.query.isAccomplish">
        <bk-divider><h3>试卷标题</h3></bk-divider>
        <h3>一、单选题</h3>
        <bk-card class="radio-common" :title="`${index + 1}.${item.name}`" v-for="(item,index) in questionList" :key="index" :border="false">
            <bk-radio-group class="radio-common" v-model="item.selectValue">
                <bk-radio v-for="(childItem,childIndex) in item.choices" :key="childIndex" :value="childItem.option" :disabled="true">
                    {{ childItem.option }}：{{ childItem.content }}
                </bk-radio>
            </bk-radio-group>
            <bk-divider></bk-divider>
            <p style="margin-top: 10px">
                你的选择：<span>a</span>
            </p>
            <p style="margin-top: 10px">
                正确答案为：<span>c</span>
            </p>
            <p style="margin-top: 10px">
                解析：<span>test</span>
            </p>
            <div style="margin-top: 10px">
                你的得分：2
            </div>
        </bk-card>

        <h3>二、多选题</h3>
        <bk-card class="radio-common" :title="`${index + 1}.${item.name}`" v-for="(item,index) in multipleQuestionList" :key="index" :border="false">
            <bk-checkbox-group class="radio-common" v-model="item.selectValue">
                <bk-checkbox v-for="(childItem,childIndex) in item.choices" :key="childIndex" :value="childItem.option" :disabled="true">
                    {{ childItem.option }}：{{ childItem.content }}
                </bk-checkbox>
            </bk-checkbox-group>
            <bk-divider></bk-divider>
            <p style="margin-top: 10px">
                你的选择：<span>abc</span>
            </p>
            <p style="margin-top: 10px">
                正确答案为：<span>ac</span>
            </p>
            <p style="margin-top: 10px">
                解析：<span>test</span>
            </p>
            <div style="margin-top: 10px">
                你的得分：4
            </div>
        </bk-card>

        <h3>三、填空题</h3>
        <bk-card class="radio-common" :title="`${index + 1}.${item.name}`" v-for="(item,index) in summaryQuestionList" :key="index" :border="false">
            <p>
                你的答案：<span>{{ item.myAnswer }}</span>
            </p>
            <p style="margin-top: 10px">
                正确答案：<span>{{ item.standardAnswer }}</span>
            </p>
            <p style="margin-top: 10px">
                解析：<span>test</span>
            </p>
            <div style="margin-top: 10px">
                你的得分：2
            </div>
        </bk-card>

        <h3>四、判断题</h3>
        <bk-card class="radio-common" :title="`${index + 1}.${item.name}`" v-for="(item,index) in judgeQuestionList" :key="index" :border="false">
            <bk-radio-group class="radio-common" v-model="item.selectValue">
                <bk-radio v-for="(childItem,childIndex) in item.choices" :key="childIndex" :value="childItem.option" :disabled="true">
                    {{ childItem.option }}：{{ childItem.content }}
                </bk-radio>
            </bk-radio-group>
            <bk-divider></bk-divider>
            <p style="margin-top: 10px">
                你的选择：<span>T</span>
            </p>
            <p style="margin-top: 10px">
                正确答案为：<span>T</span>
            </p>
            <p style="margin-top: 10px">
                解析：<span>test</span>
            </p>
            <div style="margin-top: 10px">
                你的得分：2
            </div>
        </bk-card>

        <h3>五、简答题</h3>
        <bk-card class="radio-common" :title="`${index + 1}.${item.name}`" v-for="(item,index) in shortQuestionList" :key="index" :border="false">
            <p>
                你的答案：<span>{{ item.myAnswer }}</span>
            </p>
            <p style="margin-top: 10px">
                正确答案：<span>{{ item.standardAnswer }}</span>
            </p>
            <p style="margin-top: 10px">
                解析：<span>test</span>
            </p>
            <div style="margin-top: 10px">
                你的得分：20
            </div>
        </bk-card>
    </div>
    <div class="wrapper" v-else>
        <h2>试卷信息</h2>
        <div class="studentInfo">
            <span>学生班级：物网191</span>
            <span>学生姓名：白郑鑫</span>
            <span>学生学号：3190932002</span>
        </div>
        <h3>一、单选题</h3>
        <bk-card class="radio-common" :title="`${index + 1}.${item.name}`" v-for="(item,index) in questionList" :key="index" :border="false">
            <bk-radio-group class="radio-common" v-model="item.selectValue">
                <bk-radio v-for="(childItem,childIndex) in item.choices" :key="childIndex" :value="childItem.option" :disabled="true">
                    {{ childItem.option }}：{{ childItem.content }}
                </bk-radio>
            </bk-radio-group>
            <bk-divider></bk-divider>
            <div style="margin-top: 10px">
                你的选择：<span>a</span>
            </div>
            <div style="margin-top: 10px">
                正确答案为：<span>c</span>
            </div>
            <div style="margin-top: 10px">
                解析：<span>test</span>
            </div>
            <div style="margin-top: 10px">
                得分：<bk-input style="width: 150px" :clearable="true" placeholder="请输入得分"></bk-input>
            </div>
        </bk-card>

        <h3>二、多选题</h3>
        <bk-card class="radio-common" :title="`${index + 1}.${item.name}`" v-for="(item,index) in multipleQuestionList" :key="index" :border="false">
            <bk-checkbox-group class="radio-common" v-model="item.selectValue">
                <bk-checkbox v-for="(childItem,childIndex) in item.choices" :key="childIndex" :value="childItem.option" :disabled="true">
                    {{ childItem.option }}：{{ childItem.content }}
                </bk-checkbox>
            </bk-checkbox-group>
            <bk-divider></bk-divider>
            <p style="margin-top: 10px">
                你的选择：<span>abc</span>
            </p>
            <p style="margin-top: 10px">
                正确答案为：<span>ac</span>
            </p>
            <p style="margin-top: 10px">
                解析：<span>test</span>
            </p>
            <div style="margin-top: 10px">
                得分：<bk-input style="width: 150px" :clearable="true" placeholder="请输入得分"></bk-input>
            </div>
        </bk-card>

        <h3>三、填空题</h3>
        <bk-card class="radio-common" :title="`${index + 1}.${item.name}`" v-for="(item,index) in summaryQuestionList" :key="index" :border="false">
            <p>
                你的答案：<span>{{ item.myAnswer }}</span>
            </p>
            <p style="margin-top: 10px">
                正确答案：<span>{{ item.standardAnswer }}</span>
            </p>
            <p style="margin-top: 10px">
                解析：<span>test</span>
            </p>
            <div style="margin-top: 10px">
                得分：<bk-input style="width: 150px" :clearable="true" placeholder="请输入得分"></bk-input>
            </div>
        </bk-card>

        <h3>四、判断题</h3>
        <bk-card class="radio-common" :title="`${index + 1}.${item.name}`" v-for="(item,index) in judgeQuestionList" :key="index" :border="false">
            <bk-radio-group class="radio-common" v-model="item.selectValue">
                <bk-radio v-for="(childItem,childIndex) in item.choices" :key="childIndex" :value="childItem.option" :disabled="true">
                    {{ childItem.option }}：{{ childItem.content }}
                </bk-radio>
            </bk-radio-group>
            <bk-divider></bk-divider>
            <p style="margin-top: 10px">
                你的选择：<span>T</span>
            </p>
            <p style="margin-top: 10px">
                正确答案为：<span>T</span>
            </p>
            <p style="margin-top: 10px">
                解析：<span>test</span>
            </p>
            <div style="margin-top: 10px">
                得分：<bk-input style="width: 150px" :clearable="true" placeholder="请输入得分"></bk-input>
            </div>
        </bk-card>

        <h3>五、简答题</h3>
        <bk-card class="radio-common" :title="`${index + 1}.${item.name}`" v-for="(item,index) in shortQuestionList" :key="index" :border="false">
            <p>
                你的答案：<span>{{ item.myAnswer }}</span>
            </p>
            <p style="margin-top: 10px">
                正确答案：<span>{{ item.standardAnswer }}</span>
            </p>
            <p style="margin-top: 10px">
                解析：<span>test</span>
            </p>
            <div style="margin-top: 10px">
                得分：<bk-input style="width: 150px" :clearable="true" placeholder="请输入得分"></bk-input>
            </div>
        </bk-card>

        <bk-button style="width: 60px" :theme="'primary'" type="submit">提交</bk-button>

    </div>
</template>

<script>
    export default {
        name: 'answer_question_detail',
        data () {
            return {
                selectValue: 1,
                questionList: [
                    {
                        name: 'test ( )',
                        choices: [
                            {
                                option: 'A',
                                content: 'testa'
                            },
                            {
                                option: 'B',
                                content: 'testb'
                            },
                            {
                                option: 'C',
                                content: 'testc'
                            },
                            {
                                option: 'D',
                                content: 'testd'
                            }
                        ],
                        selectValue: 'A'
                    },
                    {
                        name: 'test ( )',
                        choices: [
                            {
                                option: 'A',
                                content: 'testa'
                            },
                            {
                                option: 'B',
                                content: 'testb'
                            },
                            {
                                option: 'C',
                                content: 'testc'
                            },
                            {
                                option: 'D',
                                content: 'testd'
                            }
                        ],
                        selectValue: 'A'
                    },
                    {
                        name: 'test ( )',
                        choices: [
                            {
                                option: 'A',
                                content: 'testa'
                            },
                            {
                                option: 'B',
                                content: 'testb'
                            },
                            {
                                option: 'C',
                                content: 'testc'
                            },
                            {
                                option: 'D',
                                content: 'testd'
                            }
                        ],
                        selectValue: 'A'
                    },
                    {
                        name: 'test ( )',
                        choices: [
                            {
                                option: 'A',
                                content: 'testa'
                            },
                            {
                                option: 'B',
                                content: 'testb'
                            },
                            {
                                option: 'C',
                                content: 'testc'
                            },
                            {
                                option: 'D',
                                content: 'testd'
                            }
                        ],
                        selectValue: 'A'
                    },
                    {
                        name: 'test ( )',
                        choices: [
                            {
                                option: 'A',
                                content: 'testa'
                            },
                            {
                                option: 'B',
                                content: 'testb'
                            },
                            {
                                option: 'C',
                                content: 'testc'
                            },
                            {
                                option: 'D',
                                content: 'testd'
                            }
                        ],
                        selectValue: 'A'
                    }
                ],
                multipleQuestionList: [
                    {
                        name: 'test ( )',
                        choices: [
                            {
                                option: 'A',
                                content: 'testa'
                            },
                            {
                                option: 'B',
                                content: 'testb'
                            },
                            {
                                option: 'C',
                                content: 'testc'
                            },
                            {
                                option: 'D',
                                content: 'testd'
                            }
                        ],
                        selectValue: ['A', 'B', 'C']
                    },
                    {
                        name: 'test ( )',
                        choices: [
                            {
                                option: 'A',
                                content: 'testa'
                            },
                            {
                                option: 'B',
                                content: 'testb'
                            },
                            {
                                option: 'C',
                                content: 'testc'
                            },
                            {
                                option: 'D',
                                content: 'testd'
                            }
                        ],
                        selectValue: ['A', 'B', 'C']
                    },
                    {
                        name: 'test ( )',
                        choices: [
                            {
                                option: 'A',
                                content: 'testa'
                            },
                            {
                                option: 'B',
                                content: 'testb'
                            },
                            {
                                option: 'C',
                                content: 'testc'
                            },
                            {
                                option: 'D',
                                content: 'testd'
                            }
                        ],
                        selectValue: ['A', 'B', 'C']
                    },
                    {
                        name: 'test ( )',
                        choices: [
                            {
                                option: 'A',
                                content: 'testa'
                            },
                            {
                                option: 'B',
                                content: 'testb'
                            },
                            {
                                option: 'C',
                                content: 'testc'
                            },
                            {
                                option: 'D',
                                content: 'testd'
                            }
                        ],
                        selectValue: ['A', 'B', 'C']
                    },
                    {
                        name: 'test ( )',
                        choices: [
                            {
                                option: 'A',
                                content: 'testa'
                            },
                            {
                                option: 'B',
                                content: 'testb'
                            },
                            {
                                option: 'C',
                                content: 'testc'
                            },
                            {
                                option: 'D',
                                content: 'testd'
                            }
                        ],
                        selectValue: ['A', 'B', 'C']
                    }
                ],
                summaryQuestionList: [
                    {
                        name: '填空题',
                        myAnswer: '哈哈哈',
                        standardAnswer: '中国'
                    },
                    {
                        name: '填空题',
                        myAnswer: '哈哈哈',
                        standardAnswer: '中国'
                    },
                    {
                        name: '填空题',
                        myAnswer: '哈哈哈',
                        standardAnswer: '中国'
                    },
                    {
                        name: '填空题',
                        myAnswer: '哈哈哈',
                        standardAnswer: '中国'
                    },
                    {
                        name: '填空题',
                        myAnswer: '哈哈哈',
                        standardAnswer: '中国'
                    }
                ],
                judgeQuestionList: [
                    {
                        name: '判断一下对不对',
                        choices: [
                            {
                                option: 'T',
                                content: 'testa'
                            },
                            {
                                option: 'F',
                                content: 'testb'
                            }
                        ],
                        selectValue: 'T'
                    },
                    {
                        name: '判断一下对不对',
                        choices: [
                            {
                                option: 'T',
                                content: 'testa'
                            },
                            {
                                option: 'F',
                                content: 'testb'
                            }
                        ],
                        selectValue: 'T'
                    },
                    {
                        name: '判断一下对不对',
                        choices: [
                            {
                                option: 'T',
                                content: 'testa'
                            },
                            {
                                option: 'F',
                                content: 'testb'
                            }
                        ],
                        selectValue: 'T'
                    },
                    {
                        name: '判断一下对不对',
                        choices: [
                            {
                                option: 'T',
                                content: 'testa'
                            },
                            {
                                option: 'F',
                                content: 'testb'
                            }
                        ],
                        selectValue: 'T'
                    },
                    {
                        name: '判断一下对不对',
                        choices: [
                            {
                                option: 'T',
                                content: 'testa'
                            },
                            {
                                option: 'F',
                                content: 'testb'
                            }
                        ],
                        selectValue: 'T'
                    }
                ],
                shortQuestionList: [
                    {
                        name: '简答题题目',
                        myAnswer: '我的答案',
                        standardAnswer: '标准答案'
                    },
                    {
                        name: '简答题题目',
                        myAnswer: '我的答案',
                        standardAnswer: '标准答案'
                    },
                    {
                        name: '简答题题目',
                        myAnswer: '我的答案',
                        standardAnswer: '标准答案'
                    }
                ]
            }
        },
        mounted () {
            this.getQuestionList()
        },
        methods: {
            async getQuestionList () {
                this.$http.get('/course/manage_paper_question_contact/', { params: { paper_id: this.$route.query.id, flag: 1 } }).then(res => {
                    console.log(res)
                })
            }
        }
    }
</script>

<style scoped>
.wrapper {
    display: flex;
    flex-direction: column;
    height: 580px;
    overflow-y: auto;
}

.radio-common {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    box-shadow: none;
}

.studentInfo {
    display: flex;
    align-items: center;
    justify-content: space-around;
}
</style>
