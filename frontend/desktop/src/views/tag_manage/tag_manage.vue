<template>
    <div id="tag_manage">
        <tag v-for="tag in tags" :key="tag">{{tag}}</tag>
    </div>
</template>

<script>
    const tag = () => import('./components/tag')
    export default {
        components: { tag },
        omponents: {
            tag
        },
        data () {
            return {
                tags: ['ck', 'mc', 'zyz', 'wyc', 'ljy']
            }
        }
    }
</script>

<style>
</style>
