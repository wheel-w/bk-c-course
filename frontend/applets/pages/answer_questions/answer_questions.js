let cids = []//题号数组
var url='http://dev.paas-edu.bktencent.com:8000/'+wx.getStorageSync('url')
const app=getApp()
Page({
  data:{
    pingData: [{
      "time": "1799000",
    }],
    stu:[{
      questions_id:Array(),
      stu_answers:Array(),
    }],
    total:0,
    inputValue: null,
    swi:0,
    subject:null,
    questions:null,//存题
    current: 1,//第一道题开始
  },
  onLoad(){
    this.setData({
      listData: this.data.pingData
    })
    this.setCountDown();
    var header;
    var user_id=wx.getStorageSync("user_id")
    header = {
      'content-type':'application/x-www-form-urlencoded',
      'cookie':wx.getStorageSync("states")
    }
    wx.request({
      url: url,
      method:'GET',
      header: header,
      data:{
        user_id: user_id,
      },
      success: res => {
        let questions = res.data.data.titles//取题库
        app.globalData.questions = res.data.data.titles
        cids = res.data.data.cids
        let subject= questions[0]//第一组
        cids = res.data.data.cids
        wx.setStorageSync('cids', cids)
        app.globalData.total = res.data.data.titles.length
        this.setData({
          questions: questions,
          subject: subject,
          total: res.data.data.titles.length,
        })
      }
    })
   
  },
  //用户选择
  moreClick(e){
    var nums = e.detail.value
    var index = this.data.current-1
    var replace1 = 'stu['+index+'].stu_answers'
    var replace2 = 'stu['+index+'].questions_id'
    let cid = cids[index]
    for (var i = 0; i < 4; i++) {
      if(nums[i]=='A'){
        var replace3 = 'subject.options[0].selected'
        this.setData({[replace3]: true,})
      }
      if(nums[i]=='B'){
        var replace3 = 'subject.options[1].selected'
        this.setData({[replace3]: true,})
      }
      if(nums[i]=='C'){
        var replace3 = 'subject.options[2].selected'
        this.setData({[replace3]: true,})
      }
      if(nums[i]=='D'){
        var replace3 = 'subject.options[3].selected'
        this.setData({[replace3]: true,})
      }
    }
    this.setData({
      [replace1]: e.detail.value,
      [replace2]: cid,
    })
    app.globalData.stu= this.data.stu
  },
  Click(e){
    if(e.detail.value=='A')
      {      
        var num = 0
      }
    if(e.detail.value=='B')
      {  
        var num = 1
      }
    if(e.detail.value=='C')
      {
        var num = 2
      }
    if(e.detail.value=='D')
      {
        var num = 3
      }
    var index = this.data.current-1
    var replace1 = 'stu['+index+'].stu_answers'
    var replace2 = 'stu['+index+'].questions_id'
    var replace3 = 'subject.options['+num+'].selected'
    let cid = cids[index]
    this.setData({
      [replace1]: e.detail.value,
      [replace2]: cid,
      [replace3]: true,
    })
    app.globalData.stu = this.data.stu
  },
  Write(e){
    var index = this.data.current-1
    var replace1 = 'stu['+index+'].stu_answers'
    var replace2 = 'stu['+index+'].questions_id'
    let cid = cids[index]

    this.setData({
      [replace1]: e.detail.value,
      [replace2]: cid,
    })
    app.globalData.stu = this.data.stu
  },
  preclearInputEvent: function(res) {
    //swi:0
    if(this.data.current-2 < 0 || this.data.swi-1 < 0){
      wx.showToast({
        icon:'none',
        title: '已经是第一题了',
      })
      return
    }
    if(this.data.stu[this.data.swi-1]==undefined)
    {
      this.setData({'inputValue': '',})
    }
    else{
      this.setData({'inputValue': this.data.stu[this.data.swi-1].stu_answers,})
    }
    this.setData({
      subject: this.data.questions[this.data.swi-1],
      current: this.data.current-1,
      swi: this.data.swi-1,
    })
    app.globalData.stu = this.data.stu
  },
  nextclearInputEvent: function(res) {
    // swi:0,
    if(this.data.current+1>this.data.total){
      wx.showToast({
        icon:'none',
        title: '已经是最后一题了。',
      })
      return
    }
    if(this.data.stu[this.data.swi+1]==undefined)
    {
      this.setData({'inputValue': '',})
    }
    else{
      this.setData({'inputValue': this.data.stu[this.data.swi+1].stu_answers,})
    }
    this.setData({
      current: this.data.current+1,
      swi: this.data.swi+1,
      subject: this.data.questions[this.data.swi+1],
    })
    app.globalData.stu = this.data.stu
  },
  pre(){
    //swi:0
    if(this.data.current-2 < 0 || this.data.swi-1 < 0){
      wx.showToast({
        icon:'none',
        title: '已经是第一题了',
      })
      return
    }
    this.setData({
      subject: this.data.questions[this.data.swi-1],
      current: this.data.current-1,
      swi: this.data.swi-1,
    })
  },
  next(){
      // swi:0,
    if(this.data.current+1>this.data.total){
      wx.showToast({
        icon:'none',
        title: '已经是最后一题了。',
      })
      return
    }
    this.setData({
      current: this.data.current+1,
      swi: this.data.swi+1,
      subject: this.data.questions[this.data.swi+1],
    })
  },
  card(){
    wx.navigateTo({
      url: '/pages/answer_card/answer_card',
    })
  },
  submit(){

  },
  // 倒计时
  setCountDown: function () {
    let time = 1000;
  let { listData } = this.data;
    let list = listData.map((v, i) => {
      if (v.time <= 0) {
        v.time = 0;
      }
      let formatTime = this.getFormat(v.time);
      v.time -= time;
      v.countDown = `${formatTime.mm}:${formatTime.ss}`;
      return v;
    })
    this.setData({
      listData: list
    });
    setTimeout(this.setCountDown, time);
  },
   // 格式化时间
  getFormat: function (msec) {
    let ss = parseInt(msec / 1000);
    let mm = 0;
    if (ss > 60) {
      mm = parseInt(ss / 60);
      ss = parseInt(ss % 60);
      if (mm > 60) {
        mm = parseInt(mm % 60);
      }
    }
    ss = ss > 9 ? ss : `0${ss}`;
    mm = mm > 9 ? mm : `0${mm}`;
    return {
      ss,
      mm,
    };
  }
})
