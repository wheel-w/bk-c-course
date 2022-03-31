App({
  globalData: {
    url : 'https://apps.paas-edu.bktencent.com/stag--bk-course-manage/set_question_index/'

  },
  onLoad(){
  },
  onLaunch() {
    // 登录
    wx.login({
      success: res => {
        if(res.code){
          // 将code发送到后端
          wx.request({
            url: 'https://apps.paas-edu.bktencent.com/stag--bk-course-manage/account/get_user_info/',
            data: {
              'code': res.code,
            },
            header: {
              'content-type': 'application/json' // 默认值
            },
            success(res){
              console.log(res.data)
              wx.setStorageSync('name', res.data.data.name)
              if(res.data.data.identity!='NOT_CERTIFIED'){
                let state = res.data.data.state;
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