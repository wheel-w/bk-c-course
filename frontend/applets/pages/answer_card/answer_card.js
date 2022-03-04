const app = getApp()
Page({
  data: {
    list:[],
  },
  onLoad: function (options) {
    let that = this
    let stu = app.globalData.stu
    let total = app.globalData.total
    let questionList = []
    if(stu==undefined){
      for (let i = 0; i < total; i++) {
        let item = {}
        item.index = i
        item.done = false
        questionList.push(item)
      }
      that.setData({
        list: questionList
      })
    }
    else{
      for (let i = 0; i < total; i++) {
  
        let item = {}
        item.index = i
        if(stu[0].stu_answers.length==0){
          item.done = false
        }
        else{
          item.done = true
        }
        if(i>=1){
          if(stu[i]==undefined){
            item.done = false
          }
          else{
            item.done = true
          }
        }
        questionList.push(item)
      }
      that.setData({
        list: questionList
      })
    }
  },
  onClickCardItem: function (e) {
    let pages = getCurrentPages();
    let prevPage = pages[pages.length - 2];
    let questions = app.globalData.questions
    let stu = app.globalData.stu
    if(stu!=undefined){
      if(stu[e.currentTarget.dataset.index]!=undefined){
        prevPage.setData({
          inputValue: stu[e.currentTarget.dataset.index].stu_answers,
        })
      }
      else{
        prevPage.setData({
          inputValue: '',
        })
      }
    }
    prevPage.setData({
      subject: questions[e.currentTarget.dataset.index],
      current: e.currentTarget.dataset.index+1,
      swi: e.currentTarget.dataset.index,
    })
    wx.navigateBack({
      delta: 1,
    })
  }
})