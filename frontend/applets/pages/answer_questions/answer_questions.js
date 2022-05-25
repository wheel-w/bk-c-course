var util = require ( '../../utils/util.js' );
const app=getApp()
Page({
  data:{
    hours: '0' + 0,   // 时
    minute: '0' + 0,   // 分
    second: '0' + 0,   // 秒
    time: '0',
    submited:false,
    questions_bank:'',
    newStu:'',
    newQuestions_bank:'',
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
      console.log(res.data)
      var now_time = util .formatTime ( new Date ());
      var n1 = new Date(now_time)
      var n2 = new Date(res.data.data.paper_end_time)
      if((res.data.data.paper_status=="RELEASE")&&(n1-n2<=0)){
        if(((wx.getStorageSync('stu')=='')&&(wx.getStorageSync('questions')==''))||(app.globalData.tit==false)||(wx.getStorageSync('no_read')==false)){
        console.log('不读缓存')
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
          console.log(res.data)
          if(res.data.data.status=='SUBMITTED'){
            this.setData({
              submited: true
            })
          }
          else{
            this.setData({
              submited: false
            })
          }
          let datas = res.data.data
          var a = []
          for(var index in datas){
            if((index!='cumulative_time')&&(index!='status')){
              a.push(datas[index])
            }
          }
          //拼题目
          var questions_bank = []
          for(var i=0; i<a.length; i++){
            if(a[i]==undefined){
              break
            }
            questions_bank = questions_bank.concat(a[i])
          }
          console.log(questions_bank)
          this.setData({
            newQuestions_bank: questions_bank
          })
          //拼做过的stu和questions_bank的答案
          for (var i = 0; i<questions_bank.length; ++i) {  
            // console.log(i)
            var replace1 = 'newStu['+i+'].stu_answers'
            var replace2 = 'newStu['+i+'].question_id'
            var replaceA = 'newQuestions_bank['+i+'].A'
            var replaceB = 'newQuestions_bank['+i+'].B'
            var replaceC = 'newQuestions_bank['+i+'].C'
            var replaceD = 'newQuestions_bank['+i+'].D'
            var replaceE = 'newQuestions_bank['+i+'].E'
            this.setData({
              [replace1]: questions_bank[i].student_answer,
              [replace2]: questions_bank[i].id,
            })
              // console.log(questions_bank[i].types)
            if(questions_bank[i].types=='JUDGE'){
              this.setData({
                [replaceA]: false,
                [replaceB]: false,
              })
              // console.log('进入单选',questions_bank[i])
              if (questions_bank[i].student_answer == '正确'){

                this.setData({
                  [replaceA]: true,
                  [replaceB]: false,
                })
            }
            else{
              this.setData({
                [replaceA]: false,
                [replaceB]: true,
              })
            }
            if((questions_bank[i].student_answer == null)||(questions_bank[i].student_answer == '')||(questions_bank[i].student_answer == '[]')){
              this.setData({
                [replaceA]: false,
                [replaceB]: false,
              })
            }
            }
            if(questions_bank[i].types=='SINGLE'){
              this.setData({
                [replaceA]: false,
                [replaceB]: false,
                [replaceC]: false,
                [replaceD]: false,
              })
              // console.log('进入单选',questions_bank[i])
              if (questions_bank[i].student_answer == 'A'){

                this.setData({
                  [replaceA]: true,
                  [replaceB]: false,
                  [replaceC]: false,
                  [replaceD]: false,
                })
            }
            if (questions_bank[i].student_answer == 'B'){

              this.setData({
                [replaceA]: false,
                [replaceB]: true,
                [replaceC]: false,
                [replaceD]: false,
              })
          }
          if (questions_bank[i].student_answer == 'C'){
            this.setData({
              [replaceA]: false,
              [replaceB]: false,
              [replaceC]: true,
              [replaceD]: false,
            })
        }
        if (questions_bank[i].student_answer == 'D'){
          this.setData({
            [replaceA]: false,
            [replaceB]: false,
            [replaceC]: false,
            [replaceD]: true,
          })
      }
            }
            if(questions_bank[i].types=='MULTIPLE'){
              // console.log('进入多选',questions_bank[i])
              this.setData({
                [replaceA]: false,
                [replaceB]: false,
                [replaceC]: false,
                [replaceD]: false,
                [replaceE]: false,
              })
              // console.log(questions_bank[3].student_answer)
              var str = questions_bank[i].student_answer
              var arr = str
              // var arr =  eval('(' + str + ')');
              // var arr = JSON.parse(str);
              // console.log(arr)
              // console.log(arr)
              for (var j = 0; j <=20; j++) {
                // console.log(questions_bank[j])
                // console.log(questions_bank[j].student_answer)
                if(arr[j]=='A'){
                  this.setData({
                    [replaceA]: true,
                  })
                }
                if(arr[j]=='B'){
                  this.setData({
                    [replaceB]: true,
                  })
                }
                if(arr[j]=='C'){
                  this.setData({
                    [replaceC]: true,
                  })
                }
                if(arr[j]=='D'){
                  this.setData({
                    [replaceD]: true,
                  })
                }
                if(arr[j]=='E'){
                  this.setData({
                    [replaceE]: true,
                  })
                }
              }
            }
        }
          console.log(this.data.newStu)
          console.log(this.data.newQuestions_bank)
        //时间规格化
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
          var questions_bank = this.data.newQuestions_bank
          wx.setStorageSync('questions_bank', questions_bank)
          let questions = this.data.newQuestions_bank//数组暂存题目
          console.log(questions)
          // let questions = questions_bank//数组暂存题目
          var total_length = 0
          for(var k=0;k<questions.length;k++){
            total_length = total_length+k
          }
          app.globalData.questions = this.data.newQuestions_bank
          let subject= questions[0]//第一题
          app.globalData.total = questions.length//题目总数
          this.setData({
            questions: questions,
            subject: subject,
            total: app.globalData.total,
            total_length: total_length,
            stu: this.data.newStu
          })
          app.globalData.stu= this.data.stu
          var ans= 0
          console.log(this.data.stu)
          for(var index in this.data.stu){
            if((this.data.stu[index].stu_answers!='[]')&&(this.data.stu[index].stu_answers!='')&&(this.data.stu[index].stu_answers!=null)){
              ans = ans+parseInt(index)
            }
          }
          console.log(ans)
          console.log(this.data.stu)
          console.log(this.data.total_length)
          if((ans==this.data.total_length)&&(this.data.stu[0].stu_answers!='[]')&&(this.data.stu[0].stu_answers)!=''){
            this.setData({
              can_submit : true
            })
          }
          

      }
          })
          }
          else{
            console.log('读缓存')
            console.log(wx.getStorageSync('paper_id'))
            var questions_bank = wx.getStorageSync('questions_bank')
            console.log(questions_bank)
            let questions = wx.getStorageSync('questions')//数组暂存题目
            console.log(questions)
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
              total_length: total_length,
              time: wx.getStorageSync('time'),
              can_submit: wx.getStorageSync('can_submit')
            })
            app.globalData.stu = wx.getStorageSync('stu')
          //时间规格化
          let a1 = 0
          let b1 = 0
          let c1 = 0
          var time = wx.getStorageSync('time')
          if(time!=0){
          if(time/3600>0){
            a1 = Math.floor(time/3600)
            if (b1 < 10) {
              // 少于10补零
              a1 = '0' + a1
          } 
          }
          if(time-3600*a1>0){
            b1=Math.floor((time-3600*a1)/60)
            if (b1 < 10) {
              // 少于10补零
              b1 = '0' + b1
          } 
          }
          if(time-3600*a1-60*b1>0){
            c1=Math.floor(time-3600*a1-60*b1)
            if (c1 < 10) {
              // 少于10补零
              c1 = '0' + c1
          } 
          }
          this.setData({
            hours: a1,   // 时
            minute: b1,   // 分
            second: c1,   // 秒
          })
        }
          }
      }
      else{
        if(res.data.data.paper_statu!="RELEASE"){
          wx.showModal({
            title:'获取失败',
            content:'试卷未发布',
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
      }
    }).catch(res =>{

    }) 
  },
  subImg(){
    this.data.stu2 = this.data.stu
    for (var i = 0; i < this.data.stu2.length; ++i) {  
      if((this.data.stu2[i]==undefined)||(this.data.stu2[i]==null)){
        var replace1 = 'stu2['+i+'].stu_answers'
        this.setData({
          [replace1]: null,
        })
      }
    }
  },
  onLoad(){
  this.useImage() 
  this.setInterval()
  if(this.data.submited==true){
    this.setData({
      can_submit :false
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
    console.log(this.data.stu)
    for(var index in this.data.stu){
      if((this.data.stu[index].stu_answers!='[]')&&(this.data.stu[index].stu_answers!='')&&(this.data.stu[index].stu_answers!=null)){
        ans = ans+parseInt(index)
      }
    }
    if((ans==this.data.total_length)&&(this.data.stu[0].stu_answers!='[]')&&(this.data.stu[0].stu_answers)!=''){
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
    console.log(this.data.stu)
    for(var index in this.data.stu){
      if((this.data.stu[index].stu_answers!='[]')&&(this.data.stu[index].stu_answers!='')&&(this.data.stu[index].stu_answers!=null)){
        ans = ans+parseInt(index)
      }
    }
      if((ans==this.data.total_length)&&(this.data.stu[0].stu_answers!='[]')&&(this.data.stu[0].stu_answers)!=''){
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
    })
    app.globalData.stu = this.data.stu
    var ans= 0
    console.log(this.data.stu)
    for(var index in this.data.stu){
      console.log(index)
      if((this.data.stu[index].stu_answers!='[]')&&(this.data.stu[index].stu_answers!='')&&(this.data.stu[index].stu_answers!=null)){
        ans = ans+parseInt(index)
      }
    }
    console.log(this.data.stu[0].stu_answers!='[]')
    console.log(this.data.stu[0].stu_answers!='')
    if((ans==this.data.total_length)&&(this.data.stu[0].stu_answers!='[]')&&(this.data.stu[0].stu_answers)!=''){
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
    console.log(this.data.stu)
    for(var index in this.data.stu){
      if((this.data.stu[index].stu_answers!='[]')&&(this.data.stu[index].stu_answers!='')&&(this.data.stu[index].stu_answers!=null)){
        ans = ans+parseInt(index)
      }
    }
    console.log(ans)
    console.log(this.data.total_length)
    if(ans==this.data.total_length){
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
    var no_read = false
    wx.setStorageSync('no_read', no_read)
    var url = app.globalData.url+'config-query/course/save_answer/'
    var header;
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
        answer_info: this.data.stu,
        save_or_submit: 0,
      },
      success: res => {
        console.log(res.data)
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
    if(this.data.stu[0].stu_answers=='')
    {
      this.setData({
        'stu[0].stu_answers' : null,
        // 'stu[0].question_id' : null
      })
    }
    this.subImg()
    wx.setStorageSync('questions', this.data.questions)
    console.log(this.data.questions)
    wx.setStorageSync('stu', this.data.stu)
    console.log(this.data.stu)
    wx.setStorageSync('can_submit', this.data.can_submit)
    wx.setStorageSync('time', this.data.time)
    var header;
    var url = app.globalData.url+'config-query/course/save_answer/'
    let paper_id=app.globalData.paper_id
    console.log(this.data.stu2)
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
