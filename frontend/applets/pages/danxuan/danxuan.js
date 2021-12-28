//题库
let titles = []
let errorOptions = []
const app=getApp()
Page({
  data:{
    total:0,
    totalError:0,//用户错题数
    isSelect:false,
    subject:null,
    questions:null,//存题
    current: 1,//第一道题开始
    userSelect:'',
  },
  onLoad(){
    var header;
    header = {
      'content-type':'application/x-www-form-urlencoded',
      'cookie':wx.getStorageSync("states")
    }
    wx.request({
      url: 'http://dev.paas-edu.bktencent.com:8000/weixin/question',
      method:'POST',
      header: header,
      success: res => {
        let questions = res.data.data.titles
        let subject= questions[0]
        this.setData({
          questions: questions,
          subject: subject,
          total: res.data.data.titles.length
        })
      }
    })
   
  },
  //用户选择
  radioChange(e){
    this.setData({
      userSelect:e.detail.value,
    })
  },
  submit(){
    //获取用户选项并判空
    let userSelect=this.data.userSelect
    if(!userSelect){
      wx.showToast({
        icon:'none',
        title: '请做选择',
      })
      return
    }
    let currentNum=this.data.current
    //判断用户是否答对
    if(this.data.subject.answer.indexOf(userSelect)>-1){
    }
    else{
      //记录错题
      let subjectNow = this.data.subject
      subjectNow.userSelect=userSelect
      errorOptions.push(subjectNow)
    }
    if(currentNum+1>this.data.total){
      this.setData({
        totalError:errorOptions.length
      })
      wx.showToast({
        icon:'none',
        title: '已经最后一道了',
      })
      return
    }
    let subject=this.data.questions[currentNum]
    this.setData({
      userSelect:'',
      subject:subject,
      current: currentNum+1,
      isSelect:false
    })
  },
  //查看错题集

  seeError(){
    //跳转存数据
    wx.setStorageSync('error', errorOptions)
   //app.globalData.globalErrorOptions = errorOptions
   //tabbar跳转
   wx.switchTab({
     url: '/pages/errorOptions/errorOptions',
   })
  }
})
