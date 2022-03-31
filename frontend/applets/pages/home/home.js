const app=getApp()
Page({
  data: {
    // scanCode:'扫码',
    name:'',
    cardCur: 0,
    swiperList: [{
      id: 0,
      type: 'image',
      src: "/images/landscape1.png"
      // url: 'https://ossweb-img.qq.com/images/lol/web201310/skin/big84000.jpg'
    }, {
      id: 1,
      type: 'image',
      src: "/images/landscape2.png"
        // url: 'https://ossweb-img.qq.com/images/lol/web201310/skin/big84001.jpg',
    }, {
      id: 2,
      type: 'image',
      src: "/images/landscape3.png"
      // url: 'https://ossweb-img.qq.com/images/lol/web201310/skin/big39000.jpg'
    }, {
      id: 3,
      type: 'image',
      src: "/images/landscape4.png"
      // url: 'https://ossweb-img.qq.com/images/lol/web201310/skin/big10001.jpg'
    // }, {
    //   id: 4,
    //   type: 'image',
    //   src: "/images/bg.jpg"
    //   // url: 'https://ossweb-img.qq.com/images/lol/web201310/skin/big25011.jpg'
    // }, {
    //   id: 5,
    //   type: 'image',
    //   src: "/images/bg.jpg"
    //   // url: 'https://ossweb-img.qq.com/images/lol/web201310/skin/big21016.jpg'
    // }, {
    //   id: 6,
    //   type: 'image',
    //   src: "/images/bg.jpg"
    //   // url: 'https://ossweb-img.qq.com/images/lol/web201310/skin/big99008.jpg'
    // }],
    }],
  },
  onTabItemTap(item) {
    if(item.index==1)
    this.scanCodeEvent()
  },
  onLoad: function (options) {
    this.towerSwiper('swiperList');
    this.setData({
      name: wx.getStorageSync('name')
    })
    // 初始化towerSwiper 传已有的数组名即可
  },
  scanCode() {
    wx.scanCode({
      success(res) {
        console.log(res)
        app.globalData.paper_id = res.result
        if(wx.getStorageSync('paper_id')==res.result){
          app.globalData.tit = true
        }
        else{
          app.globalData.tit = false
        }
        wx.setStorageSync('paper_id', app.globalData.paper_id)
        wx.navigateTo({
          url: '/pages/answer_questions/answer_questions',
        })
      }
    })
  },
  DotStyle(e) {
    this.setData({
      DotStyle: e.detail.value
    })
  },
  // cardSwiper
  cardSwiper(e) {
    this.setData({
      cardCur: e.detail.current
    })
  },
  // towerSwiper
  // 初始化towerSwiper
  towerSwiper(name) {
    let list = this.data[name];
    for (let i = 0; i < list.length; i++) {
      list[i].zIndex = parseInt(list.length / 2) + 1 - Math.abs(i - parseInt(list.length / 2))
      list[i].mLeft = i - parseInt(list.length / 2)
    }
    this.setData({
      swiperList: list
    })
  },
  // towerSwiper触摸开始
  towerStart(e) {
    this.setData({
      towerStart: e.touches[0].pageX
    })
  },
  // towerSwiper计算方向
  towerMove(e) {
    this.setData({
      direction: e.touches[0].pageX - this.data.towerStart > 0 ? 'right' : 'left'
    })
  },
  // towerSwiper计算滚动
  towerEnd(e) {
    let direction = this.data.direction;
    let list = this.data.swiperList;
    if (direction == 'right') {
      let mLeft = list[0].mLeft;
      let zIndex = list[0].zIndex;
      for (let i = 1; i < list.length; i++) {
        list[i - 1].mLeft = list[i].mLeft
        list[i - 1].zIndex = list[i].zIndex
      }
      list[list.length - 1].mLeft = mLeft;
      list[list.length - 1].zIndex = zIndex;
      this.setData({
        swiperList: list
      })
    } else {
      let mLeft = list[list.length - 1].mLeft;
      let zIndex = list[list.length - 1].zIndex;
      for (let i = list.length - 1; i > 0; i--) {
        list[i].mLeft = list[i - 1].mLeft
        list[i].zIndex = list[i - 1].zIndex
      }
      list[0].mLeft = mLeft;
      list[0].zIndex = zIndex;
      this.setData({
        swiperList: list
      })
    }
  }
})