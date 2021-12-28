App({
  globalData: {
  },
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    // 登录
    wx.login({
      success: res => {
        if(res.code){
          // 将code发送到后端
          wx.request({
            url: 'http://dev.paas-edu.bktencent.com:8000/weixin/login',
            data: {
              code: res.code,
            },
            header: {
              'content-type': 'application/json' // 默认值
            },
            success(res){
              if(res.data.result){
                let state = res.data.state;
                wx.setStorageSync('states', state)
               wx.setStorage({
                key:'username',
                data: res.data.username,
              })
              wx.switchTab({
                url: '/pages/home/home',
              })
              }
              else{
                let state = res.data.data.state;
                wx.setStorageSync('states', state)
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