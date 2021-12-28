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

  //注册
  register() {
    var that=this;
    let name = this.data.name
    let password = this.data.password
    var header;
    header = {
      'content-type':'application/x-www-form-urlencoded',
      'cookie':wx.getStorageSync("states")
    }
    wx.request({
      url: 'http://dev.paas-edu.bktencent.com:8000/weixin/authenticate',
      method:'POST',
      data: {
        name: name,
        password: password
      },
      header: header,
      //加载中代码，未测试
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
      if(res.data.result){
        wx.showToast({
          title: res.data.message,
          icon: 'success',
          duration:2000, 
          success:function(){ 
              setTimeout(function () { 
                wx.switchTab({ 
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