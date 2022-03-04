var util = require ( '../../utils/util.js' );
const app=getApp()
Page({
  data:{
    hours: '0' + 0,   // 时
    minute: '0' + 0,   // 分
    second: '0' + 0,   // 秒
    time: '0',
    paper_end_time:'',
    paper_status:'',
    stu:[{
      question_id:Array(),
      stu_answers:Array(),
    }],
    stu2:[{
      question_id:Array(),
      stu_answers:Array(),
    }],
    total:0,
    inputValue: null,
    swi:0,
    subject:null,
    questions:null,//存题
    ddl:0,
    a:[],
    b:[],
    can_submit:false,
    current: 1,//第一道题开始,
    total_length: 0,
  },
  getImgUrl() {
    var url2 = app.globalData.url+'course/get_paper_status/'
    var header;
    let paper_id=app.globalData.paper_id
    header = {
      'content-type':'application/x-www-form-urlencoded',
      'state':wx.getStorageSync("states")
    }
    return new Promise((resolve, reject) => {
      wx.request({
        url: url2,
        method:'GET',
        header: header,
        data:{
          paper_id: paper_id
        },
        success: res => {
          this.setData({
            paper_status: res.data.data.paper_status,
            paper_end_time: res.data.data.paper_end_time,
          })
          resolve(res)
        },
        fail: res => {
          reject(res)
        }
      })
    })
  },
  useImage() {
    this.getImgUrl().then(res => {
      var now_time = util .formatTime ( new Date ());
      var n1 = new Date(now_time)
      var n2 = new Date(res.data.data.paper_end_time)
      //<=c才对
      if((res.data.data.paper_status=="RELEASE")&&(n1-n2<=0)){
        var header;
        var url = app.globalData.url+'course/answer_or_check_paper/'
        let paper_id=app.globalData.paper_id
        header = {
          'content-type':'application/x-www-form-urlencoded',
          'state':wx.getStorageSync("states")
        }
          wx.request({
            url: url,
            method:'GET',
            header: header,
            data:{
              paper_id: paper_id
            },
            success: res => {
            let a1 = 0
            let b1 = 0
            let c1 = 0
            if(res.data.data.cumulative_time!=0){
            if(res.data.data.cumulative_time/3600>0){
              a1 = Math.floor(res.data.data.cumulative_time/3600)
              if (b1 < 10) {
                // 少于10补零
                a1 = '0' + a1
            } 
            }
            if(res.data.data.cumulative_time-3600*a1>0){
              b1=Math.floor((res.data.data.cumulative_time-3600*a1)/60)
              if (b1 < 10) {
                // 少于10补零
                b1 = '0' + b1
            } 
            }
            if(res.data.data.cumulative_time-3600*a1-60*b1>0){
              c1=Math.floor(res.data.data.cumulative_time-3600*a1-60*b1)
              if (c1 < 10) {
                // 少于10补零
                c1 = '0' + c1
            } 
            }
            this.setData({
              hours: a1,   // 时
              minute: b1,   // 分
              second: c1,   // 秒
              time: res.data.data.cumulative_time,
            })
          }
              if((wx.getStorageSync('stu')=='')&&(wx.getStorageSync('questions')=='')){
              let datas = res.data.data
              var a = []
              var b = []
              var c = []
              for(var index in datas){
                if(index!='cumulative_time'){
                  a.push(datas[index])
                  b.push(index)
                  c.push(datas[index].length)
                }
              }
              var questions_bank = []
              var x = []
              for(var i=0; i<=999; i++){
                if(a[i]==undefined){
                  break
                }
                questions_bank = questions_bank.concat(a[i])
                x.push(a[i].length)
              }
              wx.setStorageSync('questions_bank', questions_bank)
              let questions = questions_bank//数组暂存题目
              var total_length = 0
              for(var k=0;k<questions.length;k++){
                total_length = total_length+k
              }
              app.globalData.questions = questions_bank
              let subject= questions[0]//第一题
              app.globalData.total = questions.length//题目总数
              this.setData({
                a: a,
                b: b,
                questions: questions,
                subject: subject,
                total: app.globalData.total,
                total_length: total_length
              })
      
            }
            else{
              var questions_bank = wx.getStorageSync('questions_bank')
              let questions = wx.getStorageSync('questions')//数组暂存题目
              var total_length = 0
              for(var k=0;k<questions.length;k++){
                total_length = total_length+k
              }
              app.globalData.questions = questions_bank
              let subject= questions[0]//第一题
              app.globalData.total = questions.length//题目总数
              this.setData({
                questions: questions,
                subject: subject,
                total: app.globalData.total,
                stu: wx.getStorageSync('stu'),
                total_length: total_length
              })
            }
          }
          })
          }
      else{
        wx.showModal({
          title:'获取失败',
          content:'答题时间已过',
          showCancel:false,
          cancelColor: 'cancelColor',
          success (res) {
            if(res.confirm==true){
              wx.navigateTo({
                url: '/pages/home/home',
              })
            }
          }
        })
      }
    }).catch(res =>{

    }) 
  },
  subImg(){
    this.data.stu2 = this.data.stu
    for (var i = 0; i < this.data.stu2.length; ++i) {  
      if((this.data.stu2[i]==undefined)||(this.data.stu2[i]==null)){
        var replace1 = 'stu2['+i+'].stu_answers'
        var replace2 = 'stu2['+i+'].question_id'
        this.setData({
          [replace1]: null,
          [replace2]: null,
        })
      }
    }
  },
  onLoad(){
  this.useImage() 
  this.setInterval()
  if(wx.getStorageSync('stu')!=''){
    app.globalData.stu = wx.getStorageSync('stu')
  }
  if(wx.getStorageSync('can_submit')!=''){
      this.setData({
        can_submit: wx.getStorageSync('can_submit')
      })
  }
  },
  judgeClick(e){
    if(e.detail.value=='正确')
      {      
        this.setData({
          'subject.A':true,
          'subject.B':null,
        })
      }
    if(e.detail.value=='错误')
      {  
        this.setData({
          'subject.A':null,
          'subject.B':true,
        })
      }
    var index = this.data.current-1
    var replace1 = 'stu['+index+'].stu_answers'
    var replace2 = 'stu['+index+'].question_id'
    let cid = this.data.subject.id
    this.setData({
      [replace1]: e.detail.value,
      [replace2]: cid,
    })
    app.globalData.stu = this.data.stu
    var ans= 0
    for(var index in this.data.stu){
      ans = ans+parseInt(index)
    }
    if((this.data.stu[0].question_id!='')&&(ans==this.data.total_length)){
      this.setData({
        can_submit : true
      })
    }
  },
  moreClick(e){
    this.setData({
      'subject.A':false,
      'subject.B':false,
      'subject.C':false,
      'subject.D':false,
    })
    var nums = e.detail.value
    var index = this.data.current-1
    var replace1 = 'stu['+index+'].stu_answers'
    var replace2 = 'stu['+index+'].question_id'
    let cid = this.data.subject.id
    for (var i = 0; i < 4; i++) {
      if(nums[i]=='A'){
        this.setData({
          'subject.A':true,
        })
      }
      if(nums[i]=='B'){
        this.setData({
          'subject.B':true,
        })
      }
      if(nums[i]=='C'){
        this.setData({
          'subject.C':true,
        })
      }
      if(nums[i]=='D'){
        this.setData({
          'subject.D':true,
        })
      }
      if(nums[i]=='E'){
        this.setData({
          'subject.E':true,
        })
      }
    }
    this.setData({
      [replace1]: e.detail.value,
      [replace2]: cid,
    })
    app.globalData.stu= this.data.stu
    var ans= 0
    for(var index in this.data.stu){
      ans = ans+parseInt(index)
    }
    if((this.data.stu[0].question_id!='')&&(ans==this.data.total_length)){
      this.setData({
        can_submit : true
      })
    }
  },
  Click(e){
    if(e.detail.value=='A')
      {      
        // var num = 0
        this.setData({
          'subject.A':true,
          'subject.B':null,
          'subject.C':null,
          'subject.D':null,
        })
      }
    if(e.detail.value=='B')
      {  
        // var num = 1
        this.setData({
          'subject.A':null,
          'subject.B':true,
          'subject.C':null,
          'subject.D':null,
        })
      }
    if(e.detail.value=='C')
      {
        // var num = 2
        this.setData({
          'subject.A':null,
          'subject.B':null,
          'subject.C':true,
          'subject.D':null,
        })
      }
    if(e.detail.value=='D')
      {
        // var num = 3
        this.setData({
          'subject.A':null,
          'subject.B':null,
          'subject.C':null,
          'subject.D':true,
        })
      }
    var index = this.data.current-1
    var replace1 = 'stu['+index+'].stu_answers'
    var replace2 = 'stu['+index+'].question_id'
    let cid = this.data.subject.id
    this.setData({
      [replace1]: e.detail.value,
      [replace2]: cid,
      // [replace3]: true,
    })
    app.globalData.stu = this.data.stu
    var ans= 0
    for(var index in this.data.stu){
      ans = ans+parseInt(index)
    }
    if((this.data.stu[0].question_id!='')&&(ans==this.data.total_length)){
      this.setData({
        can_submit : true
      })
    }
  },
  Write(e){
    var index = this.data.current-1
    var replace1 = 'stu['+index+'].stu_answers'
    var replace2 = 'stu['+index+'].question_id'
    let cid = this.data.subject.id

    this.setData({
      [replace1]: e.detail.value,
      [replace2]: cid,
    })
    app.globalData.stu = this.data.stu
    var ans= 0
    for(var index in this.data.stu){
      ans = ans+parseInt(index)
    }
    if((this.data.stu[0].question_id!='')&&(ans==this.data.total_length)){
      this.setData({
        can_submit : true
      })
    }
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
    if(this.data.stu[this.data.current-2]==undefined)
    {
      this.setData({'inputValue': '',})
    }
    else{
      this.setData({'inputValue': this.data.stu[this.data.current-2].stu_answers,})
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
      if(this.data.stu[this.data.current]==undefined)
      {
        this.setData({'inputValue': '',})
      }
      else{
        this.setData({'inputValue': this.data.stu[this.data.current].stu_answers,})
      }
      this.setData({
        current: this.data.current+1,
        swi: this.data.swi+1,
        subject: this.data.questions[this.data.swi+1],
      })
    app.globalData.stu = this.data.stu
  },
  pre(){
    // swi:0
    if(this.data.current-2 < 0 || this.data.swi-1 < 0){
      wx.showToast({
        icon:'none',
        title: '已经是第一题了',
      })
      return
    }
    if(this.data.stu[this.data.current-2]==undefined)
    {
      this.setData({'inputValue': '',})
    }
    else{
      this.setData({'inputValue': this.data.stu[this.data.current-2].stu_answers,})
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
    if(this.data.stu[this.data.current]==undefined)
    {
      this.setData({'inputValue': '',})
    }
    else{
      this.setData({'inputValue': this.data.stu[this.data.current].stu_answers,})
    }
      this.setData({
        current: this.data.current+1,
        swi: this.data.swi+1,
        subject: this.data.questions[this.data.swi+1],
      })
    app.globalData.stu= this.data.stu
  },
  card(){
    wx.navigateTo({
      url: '/pages/answer_card/answer_card',
    })
  },
  submit(){
    var header;
    let paper_id=app.globalData.paper_id
    header = {
      'content-type': 'application/json', // 默认值
      'state':wx.getStorageSync("states")
    }
    wx.request({
      url: 'https://paas-edu.bktencent.com/t/config-query/course/save_answer/',
      method:'POST',
      header: header,
      data:{
        paper_id: paper_id,
        answer_info: this.data.stu,
        save_or_submit: 0,
      },
      success: res => {
        wx.showToast({
          title: '提交成功',
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
    })
  },
  save(){
    let g =this.data.stu.length
    if((this.data.stu[0].question_id=='')&&(this.data.stu[g-1].question_id=='')){
      wx.showToast({
        icon:'none',
        title: '请先作答',
      })
      return
    }
    if(this.data.stu[0].question_id=='')
    {
      this.setData({
        'stu[0].stu_answers' : null,
        'stu[0].question_id' : null
      })
    }
    this.subImg()
    wx.setStorageSync('questions', this.data.questions)
    wx.setStorageSync('stu', this.data.stu)
    wx.setStorageSync('can_submit', this.data.can_submit)
    var header;
    var url = app.globalData.url+'config-query/course/save_answer/'
    let paper_id=app.globalData.paper_id
    header = {
      'content-type': 'application/json', // 默认值
      'state':wx.getStorageSync("states")
    }
    wx.request({
      url: url,
      method:'POST',
      header: header,
      data:{
        cumulative_time: parseInt(this.data.time),
        paper_id: paper_id,
        answer_info: this.data.stu2,
        save_or_submit: 1,
      },
      success: res => {
        wx.showToast({
          title: '保存成功',
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
    })
  },
  setInterval: function () {
    const that = this 
    setInterval(function () {  // 设置定时器
      var second1 = that.data.second
      var minute1 = that.data.minute
      var hours1 = that.data.hours
      var time1 = that.data.time
        second1++
        time1++
        that.setData({
          time: time1
        })
        if (second1 >= 60) {
            second1 = 0  //  大于等于60秒归零
            minute1++
            if (minute1 >= 60) {
                minute1 = 0  //  大于等于60分归零
                hours1++
                if (hours1 < 10) {
                    // 少于10补零
                    that.setData({
                        hours: '0' + hours1
                    })
                } else {
                    that.setData({
                        hours: hours1
                    })
                }
            }
            if (minute1 < 10) {
                // 少于10补零
                that.setData({
                    minute: '0' + minute1
                })
            } else {
                that.setData({
                    minute: minute1
                })
            }
        }
        if (second1 < 10) {
            // 少于10补零
            that.setData({
                second: '0' + second1
            })
        } else {
            that.setData({
                second: second1
            })
        }
    }, 1000)
},
})
