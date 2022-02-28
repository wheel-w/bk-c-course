<template>
    <div class="wrapper">
        我是答题首页（展示当前课程所有的试题）
        <bk-button theme="primary" @click="startAnswer.primary.visible = true">
            开始答题
        </bk-button>
        <bk-dialog v-model="startAnswer.primary.visible" :confirm-fn="toDetail"
            theme="primary"
            :mask-close="false"
            :header-position="startAnswer.primary.headerPosition"
            title="开始答题">
            是否确认开始答题？
        </bk-dialog>
        <bk-button theme="primary" @click="viewQrCode.primary.visible = true">
            点击查看答题二维码
        </bk-button>
        <bk-dialog v-model="viewQrCode.primary.visible"
            theme="primary"
            ok-text="下载图片"
            cancel-text="关闭"
            :mask-close="false"
            :confirm-fn="saveQrCode"
            :header-position="viewQrCode.primary.headerPosition">
            <div id="qrCodeBox">
                <div class="qrcode" id="qrCode" ref="qrCodeUrl"></div><br>
                <bk-tag theme="info">请扫描上方二维码答题</bk-tag>
            </div>
        </bk-dialog>
    </div>
</template>

<script>
    import QRCode from 'qrcodejs2'
    import { bkButton, bkDialog, bkTag } from 'bk-magic-vue'
    export default {
        name: 'answer_question_index',
        components: {
            bkButton,
            bkDialog,
            bkTag
        },
        data () {
            return {
                startAnswer: {
                    primary: {
                        visible: false,
                        headerPosition: 'left'
                    }
                },
                viewQrCode: {
                    primary: {
                        visible: false,
                        headerPosition: 'left'
                    }
                }
            }
        },
        mounted () {
            this.$nextTick(function () {
                this.bindQRCode()
            })
        },
        methods: {
            toDetail () {
                this.$router.push({
                    name: 'answer_question_detail'
                })
            },
            bindQRCode: function () {
                // eslint-disable-next-line no-new
                new QRCode(this.$refs.qrCodeUrl, {
                    text: 'https://paas-edu.bktencent.com/t/config-query',
                    width: 200,
                    height: 200,
                    colorDark: '#1768ef', // 二维码颜色
                    colorLight: '#ffffff', // 二维码背景色
                    correctLevel: QRCode.CorrectLevel.L// 容错率，L/M/H
                })
            },
            saveQrCode () {
                // 找到canvas标签
                const myCanvas = document.getElementById('qrCode').getElementsByTagName('canvas')
                // 创建一个a标签节点
                const a = document.createElement('a')
                // 设置a标签的href属性（将canvas变成png图片）
                a.href = myCanvas[0].toDataURL('image/png').replace('image/png', 'image/octet-stream')
                // 设置下载文件的名字
                a.download = '答题二维码.png'
                // 点击
                a.click()
            }
        }
        
    }
</script>

<style scoped>
    #qrCodeBox{
        height: 280px;
        margin: 0 auto;
        border: 1px solid;
        border-radius: 10px;
    }
    .qrcode{
        width: 200px;
        height: 200px;
        margin: 0 auto;
        margin-top: 20px;
    }
    .qrcode img{
        margin: 0 auto;
    }
    #qrCodeBox .bk-tag{
        position: absolute;
        left: 50%;
        margin-left: -70px;
    }
    .tag-view {
        margin-top: 20px;
        margin: 0 auto;
    }
</style>
