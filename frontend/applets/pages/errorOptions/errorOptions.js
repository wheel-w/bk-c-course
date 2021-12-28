const app=getApp()
let titles = []
Page({
  data:{
    total:0,
    current:0
  },
  onLoad(){
    //本地缓存中取数据
    let arr=wx.getStorageSync('error')
    if(arr&&arr.length>0){
      titles = arr
    }
    console.log('错题页获取错题集',titles)
    this.setData({
      subject: titles[this.data.current],
      total: titles.length
    })
  },
  //上一个错题
  pre(){
    //current:0
    if(this.data.current-1 < 0){
      wx.showToast({
        icon:'error',
        title: '已经是第一题了',
      })
    }
    else{
     this.setData({
       current: this.data.current-1,
       subject: titles[this.data.current-1],
     })
    }
  },
  //下一个错题
  next(){
     //current:0
   if(this.data.current+1 >= titles.length){
     wx.showToast({
       icon:'error',
       title: '已经是最后一题了',
     })
   }
   else{
    this.setData({
      current: this.data.current+1,
      subject: titles[this.data.current+1],
    })
   }
  },
})