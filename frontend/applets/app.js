App({
  globalData: {
    url : 'https://paas-edu.bktencent.com/t/config-query/'
  },
  onLoad(){
    // app.globalData.url = 'https://paas-edu.bktencent.com/t/config-query/'

  },
  onLaunch() {
    // 展示本地存储能力
    // const logs = wx.getStorageSync('logs') || []
    // logs.unshift(Date.now())
    // wx.setStorageSync('logs', logs)
    // 登录
    wx.login({
      success: res => {
        if(res.code){
          // var url ='https://paas-edu.bktencent.com/t/config-query/'+'config-query/account/get_user_info/'
          // 将code发送到后端
          wx.request({
            url: 'https://paas-edu.bktencent.com/t/config-query/account/get_user_info/',
            // url: url,
            data: {
              'code': res.code,
            },
            header: {
              'content-type': 'application/json' // 默认值
            },
            success(res){
              console.log(res.data)
              wx.setStorageSync('name', res.data.data.name)
              // if(res.data.data.identity=='NOT_CERTIFIED'){
              //   console.log('成功')
              // }
              if(res.data.data.identity!='NOT_CERTIFIED'){
                let state = res.data.data.state;
                // console.log(res.data.data.state)
                wx.setStorageSync('states', state)
                
               wx.setStorage({
                key:'username',
                data: res.data.username,
              })
              wx.navigateTo({
                url: '/pages/home/home',
              })
              }
              else{
                let state = res.data.data.state;
                wx.setStorageSync('states', state)
                // console.log(state)
                wx.navigateTo({
                  url: '../register/register',
                })
              }
            }
          })
          
        }
        else{
          wx.showToast({
            icon:'none',
            title: '网络错误',
          })
        }
      }
    })
  },
})