//题库
let titles = []
// const titles = [{
//   title: '1+1=?',
//   answer: ['A'],
//   options:[{
//     code:'A',
//     option:'2'
//   },{
//     code:'B',
//     option:'3'
//   },{
//     code:'C',
//     option:'4'
//   },{
//     code:'D',
//     option:'5'
//   }]
// }, 
// {
//   title: '1+2=?',
//   answer: ['A'],
//   options:[{
//     code:'A',
//     option:'2'
//   },{
//     code:'B',
//     option:'3'
//   },{
//     code:'C',
//     option:'4'
//   },{
//     code:'D',
//     option:'5'
//   }]
// }]
let errorOptions = []
const app=getApp()
Page({
  data:{
    total:0,
    totalError:0,//用户错题数
    isSelect:false,
    subject:null,
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
      url: 'url',
      method:'POST',
      header: header,
      success: res => {
        let subject= titles[0]
        console.log('subject',subject)
        //that or this可能会出问题
        this.setData({
          subject: subject,
          total: titles.length
        })
      }
    })
   
  },
  //用户选择
  checkboxChange(e){
    console.log('多选题选择了',e.detail.value)
    console.log('用户的选择',userSelect)
    this.setData({
      userSelect:e.detail.value,
    })
  },
  submit(){
    //获取用户选项并判空
    let userSelect=this.data.userSelect
    console.log('用户的选择',userSelect)
    if(!userSelect||userSelect.length<1){
      wx.showToast({
        icon:'none',
        title: '请做选择',
      })
      return
    }
    let currentNum=this.data.current

    //判断用户是否答对
    console.log('用户选项',userSelect)
    console.log('正确答案',this.data.subject.answer)
    if(this.data.subject.answer.sort().toString()==userSelect.sort().toString()){
      console.log('用户答对了第'+currentNum+"道题")
    }
    else{
      //记录错题
      console.log('用户答错了第'+currentNum+"道题")
      let subjectNow = this.data.subject
      subjectNow.userSelect=userSelect
      console.log('错题',subjectNow)
      errorOptions.push(subjectNow)
    }
    if(currentNum+1>titles.length){
      console.log('用户错题集',errorOptions)
      this.setData({
        totalError:errorOptions.length
      })
      wx.showToast({
        icon:'none',
        title: '已经最后一道了',
      })
      return
    }
    let subject=titles[currentNum]
    this.setData({
      userSelect:'',
      subject:subject,
      current: currentNum+1,
      isSelect:false
    })
  },
  //查看错题集

  seeError(){
    console.log('点击了查看错题集')
    //跳转存数据
    wx.setStorageSync('error', errorOptions)
   //app.globalData.globalErrorOptions = errorOptions

   //tabbar跳转
   wx.switchTab({
     url: '/pages/errorOptions/errorOptions',
   })
  }
})
