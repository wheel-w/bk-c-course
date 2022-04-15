<template>
    <div>
        <bk-select
            :disabled="false"
            multiple
            show-select-all
            v-model="selectedUser"
            display-tag
            enable-scroll-load
            :scroll-loading="bottomLoadingOptions"
            @scroll-end="handleScrollToBottom()"
            searchable
            style="width: 250px"
        >
            <bk-option
                v-for="option in list"
                :key="option.id"
                :id="option.id"
                :name="option.name"
            >
            </bk-option>
        </bk-select>
        <button @click="handleTest">test</button>
        <bk-select
            v-model="value2"
            style="width: 250px"
            enable-scroll-load
            :scroll-loading="bottomLoadingOptions"
            @scroll-end="handleScrollToBottom"
        >
            <bk-option
                v-for="option in list2"
                :key="option.id"
                :id="option.id"
                :name="option.name"
            >
            </bk-option>
        </bk-select>
    </div>
</template>
<script>
    import { bkSelect, bkOption } from 'bk-magic-vue'

    export default {
        components: {
            bkSelect,
            bkOption
        },
        data (s) {
            return {
                selectedUser: [],
                list: [
                    { id: 1, name: '爬山' },
                    { id: 2, name: '跑步' },
                    { id: 3, name: '打球' },
                    { id: 4, name: '跳舞' },
                    { id: 5, name: '健身' },
                    { id: 6, name: '骑车' },
                    { id: 7, name: 'k8s' },
                    { id: 8, name: 'K8S' },
                    { id: 9, name: 'mesos' },
                    { id: 10, name: 'MESOS' }
                ],
                list2: [
                    { id: 1, name: '爬山' },
                    { id: 2, name: '跑步' },
                    { id: 3, name: '打球' },
                    { id: 4, name: '跳舞' },
                    { id: 5, name: '健身' },
                    { id: 6, name: '骑车' },
                    { id: 7, name: 'k8s' },
                    { id: 8, name: 'K8S' },
                    { id: 9, name: 'mesos' },
                    { id: 10, name: 'MESOS' }
                ],
                // 分页
                page: {
                    current: 1,
                    limit: 20,
                    count: 10,
                    limitList: [20]
                },
                keyWord: '',
                bottomLoadingOptions: {
                    size: 'small',
                    isLoading: false
                }
            }
        },
        // mounted () {
        //     this.getAccountlist().then((res) => {
        //         this.list = res.data.results.map((item) => {
        //             this.page.current++
        //             return {
        //                 id: item.username,
        //                 name: item.display_name + '--------' + item.departments[0].full_name
        //             }
        //         })
        //     })
        // },
        methods: {
            handleTest () {
                console.log(this.list)
            },
            getAccountlist () {
                return this.$http.get(
                    `api/user/get_account_list/?page=${this.page.current}&key=${this.keyWord}`
                )
            },
            handleScrollToBottom () {
                console.log('到底')
                this.bottomLoadingOptions.isLoading = true
                this.getAccountlist().then((res) => {
                    this.list = [
                        ...this.list,
                        ...res.data.results.map((item) => {
                            return {
                                id: item.username,
                                name:
                                    item.display_name + '--------' + item.departments[0].full_name
                            }
                        })
                    ]
                    this.bottomLoadingOptions.isLoading = false
                    this.page.current++
                })
            }
        }
    }
</script>
