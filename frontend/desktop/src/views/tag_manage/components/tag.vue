<template>
    <div class="tag">
        <div class="palette" :style="`background-color: ${tag.tag_color_rgba};`">
            <p>{{ tag.tag_value }}</p>
        </div>
        <div class="tag_info">
            <bk-popover placement="bottom-start" width="300">
                <p>所属项目：{{ tag.sub_project }}</p>
                <p>颜色：#{{ tag.tag_color.slice(-6) }}</p>
                <!-- <p>备注：{{ tag.tag_comment }}</p> -->
                <div slot="content" style="white-space: normal">
                    <div class="pt10 pb5 pl10 pr10">{{ tag }}</div>
                </div>
            </bk-popover>
            <div class="tag_menu">
                <bk-popover
                    class="dot-menu"
                    placement="bottom-start"
                    theme="dot-menu light"
                    trigger="mouseenter"
                    :arrow="false"
                    offset="15"
                    :distance="0"
                >
                    <span class="dot-menu-trigger"></span>
                    <ul class="dot-menu-list" slot="content">
                        <li class="dot-menu-item" @click="handleDelTag">删除</li>
                        <li class="dot-menu-item" @click="handleEditTag">修改</li>
                    </ul>
                </bk-popover>
            </div>
        </div>
    </div>
</template>

<script>
    import { colorTransform } from '@/common/util'
    export default {
        props: {
            tag: {
                type: Object,
                require: true
            }
        },
        mounted () {
            this.$set(
                this.tag,
                'tag_color_rgba',
                colorTransform(this.tag.tag_color, 0.8)
            )
        },
        methods: {
            delTag () {
                return this.$http.delete(`/api/tags/${this.tag.id}/`).then((res) => {
                    this.$bkMessage({
                        message: res.message,
                        theme: res.code === 0 ? 'success' : 'error'
                    })
                    this.$emit('listChange')
                })
            },
            handleDelTag () {
                this.$bkInfo({
                    type: 'warning',
                    title: '确认删除？',
                    confirmLoading: true,
                    confirmFn: async () => {
                        try {
                            await new Promise((resolve) => {
                                this.delTag().then(() => {
                                    resolve()
                                })
                            })
                            return true
                        } catch (e) {
                            console.warn(e)
                            return true
                        }
                    }
                })
            },
            handleEditTag () {
                this.$emit('updateTag', this.tag)
            }
        }
    }
</script>

<style lang="postcss">
@import "@/css/bk-dot-menu.css";
.tag {
  width: 160px;
  height: 100px;
  border-radius: 3px;
  border: 2px solid rgba(0, 0, 0, 0.1);
  background-color: rgb(239, 239, 239);
  .palette {
    width: 100%;
    height: 60%;
    border-radius: 3px;
    position: relative;
    p:first-child {
      position: absolute;
      font-size: 20px;
      font-weight: bold;
      color: rgba(0, 0, 0, 0.7);
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
    }
  }
  .tag_info {
  }
}
</style>
