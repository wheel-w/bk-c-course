<template>
    <div class="tag">
        <div
            class="palette"
            :style="`background-color: ${tag.tag_color_rgba};`"
        ></div>
        <div class="tag_info">
            <bk-popover placement="bottom-start" width="300">
                <p>标签：{{ tag.tag_value }}</p>
                <p>所属项目：{{ tag.sub_project }}</p>
                <p>颜色：#{{ tag.tag_color }}</p>
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
                            this.$bkMessage({
                                message: '删除成功',
                                theme: 'success'
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
  height: 120px;
  border-radius: 3px;
  background-color: rgb(239, 239, 239);
  .palette {
    width: 100%;
    height: 50%;
    border-radius: 3px;
  }
  /* .tag_info {
    background-color: rgb(48, 215, 207);
  } */
}
</style>
