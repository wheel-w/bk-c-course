const app=getApp()
Page({
  data: {
    name: '',
    password: '',
    state:'',
    images:{},
    loadingHidden: false
  },
  imageLoad: function(e) {
    var $width=e.detail.width,    //获取图片真实宽度
        $height=e.detail.height,
        ratio=$width/$height;    //图片的真实宽高比例
    var viewWidth=718,           //设置图片显示宽度，左右留有16rpx边距
        viewHeight=718/ratio;    //计算的高度值
     var image=this.data.images; 
     //将图片的datadata-index作为image对象的key,然后存储图片的宽高值
     image[e.target.dataset.index]={
        width:viewWidth,
        height:viewHeight
     }
     this.setData({
          images:image
     })
    },
    //获取用户名
  getName(event) {
    this.setData({
      name: event.detail.value
    })
  },
    // 获取密码
  getPassword(event) {
    this.setData({
      password: event.detail.value
    })
  },
  //注册
  register() {
    // console.log(this.data.name)
    let name = this.data.name
    var url = app.globalData.url+'config-query/course/authenticate'
    let password = this.data.password
    var header;
    header = {
      'content-type': 'application/json', // 默认值
      'state':wx.getStorageSync("states")
    }
    wx.request({
      // url: 'https://paas-edu.bktencent.com/t/config-query/course/authenticate',
      url: url,
      method:'POST',
      data: {
        'username': name,
        'password': password
      },
      header: header,
      // 加载中代码，未测试
      // if(header){
      //   wx.showLoading({
      //     title: '加载中',
      //     mask: true
      //   })
      //   setTimeout(function () {
      //     wx.hideLoading()
      //   }, 2000)
      // },
      success(res) {
        // console.log('成功')
      if(res.data.result){
        wx.showToast({
          title: res.data.message,
          icon: 'success',
          duration:2000, 
          success:function(){ 
              setTimeout(function () { 
                wx.navigateTo({ 
                      url: '../home/home'
                   }) 
               }, 2000) 
           } 
       })
      }
      else{
        wx.showToast({
          title: res.data.message,
          icon: 'error',
          duration:2000, 
          success:function(){ 
              setTimeout(function () { 
                  wx.redirectTo({ 
                      url: '../register/register'
                   }) 
               }, 2000) 
           } 
       })
      }
      },
      fail(res) {
        wx.showToast({
          title: res.data.message,
          icon: 'error',
          duration:2000, 
          success:function(){ 
              setTimeout(function () { 
                  wx.redirectTo({ 
                      url: '../register/register'
                   }) 
               }, 2000) 
           } 
       })
      }
    })
  }
})