(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[13],{106:function(t,e,n){"use strict";n.r(e);var r=n(107);var s=n.n(r);for(var a in r)if(a!=="default")(function(t){n.d(e,t,function(){return r[t]})})(a);e["default"]=s.a},107:function(t,e,n){"use strict";var r=n(0);Object.defineProperty(e,"__esModule",{value:true});e.default=void 0;var s=r(n(15));var a=r(n(16));function u(t,e){var n=typeof Symbol!=="undefined"&&t[Symbol.iterator]||t["@@iterator"];if(!n){if(Array.isArray(t)||(n=i(t))||e&&t&&typeof t.length==="number"){if(n)t=n;var r=0;var s=function t(){};return{s:s,n:function e(){if(r>=t.length)return{done:true};return{done:false,value:t[r++]}},e:function t(e){throw e},f:s}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var a=true,u=false,o;return{s:function e(){n=n.call(t)},n:function t(){var e=n.next();a=e.done;return e},e:function t(e){u=true;o=e},f:function t(){try{if(!a&&n.return!=null)n.return()}finally{if(u)throw o}}}}function i(t,e){if(!t)return;if(typeof t==="string")return o(t,e);var n=Object.prototype.toString.call(t).slice(8,-1);if(n==="Object"&&t.constructor)n=t.constructor.name;if(n==="Map"||n==="Set")return Array.from(t);if(n==="Arguments"||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))return o(t,e)}function o(t,e){if(e==null||e>t.length)e=t.length;for(var n=0,r=new Array(e);n<e;n++){r[n]=t[n]}return r}var d={name:"correct_paper",data:function t(){return{paperEmpty:false,currentPaperId:0,currentConcatId:0,totalQuestion:{},uploadData:{student_answer_list:[],student_paper_contact_id:0},currentStudentIndex:0,studentInfo:{},studentInfoList:[],notSubmittedStudentList:[],gradeCard:{visible:false,position:{top:100}}}},computed:{totalScore:function t(){var e=0;for(var n in this.totalQuestion){var r=u(this.totalQuestion[n]),s;try{for(r.s();!(s=r.n()).done;){var a=s.value;e+=parseInt(a.student_score)}}catch(t){r.e(t)}finally{r.f()}}return e}},watch:{"$store.state.currentCourseId":function t(){this.$router.replace({name:"displaypaper"})}},mounted:function t(){this.currentPaperId=this.$route.query.paperid;this.currentPaperEndTime=Date.parse(this.$route.query.endTime);this.getQuestionList()},methods:{getStudentQuestionStation:function t(){var e=this;return(0,a.default)(s.default.mark(function t(){return s.default.wrap(function t(n){while(1){switch(n.prev=n.next){case 0:e.$http.get("/course/mark_or_check_paper/",{params:{course_id:e.$store.state.currentCourseId,paper_id:e.currentPaperId,student_id:e.studentInfo.student_id}}).then(function(t){e.currentConcatId=t.data.StudentPaperContact_id;e.totalQuestion=t.data;delete e.totalQuestion["StudentPaperContact_id"];delete e.totalQuestion["total_score"];for(var n in e.totalQuestion){var r=u(e.totalQuestion[n]),s;try{for(r.s();!(s=r.n()).done;){var a=s.value;if(a.student_answer===null){a.student_answer="未作答"}}}catch(t){r.e(t)}finally{r.f()}}});case 1:case"end":return n.stop()}}},t)}))()},getQuestionList:function t(){var e=this;this.$http.get("/course/get_student_answer_info/",{params:{course_id:this.$store.state.currentCourseId,paper_id:this.currentPaperId}}).then(function(t){e.notSubmittedStudentList=t.data.not_submitted;if((new Date).getTime()>e.currentPaperEndTime){e.studentInfoList=t.data.submitted.filter(function(t){return t.status==="SUBMITTED"||t.status==="MARKED"||t.status==="SAVED"})}else{e.studentInfoList=t.data.submitted.filter(function(t){return t.status==="SUBMITTED"||t.status==="MARKED"})}if(e.studentInfoList.length===0){e.paperEmpty=true;return}e.studentInfo=e.studentInfoList[0];e.currentStudentIndex=0;e.getStudentQuestionStation()})},checkAnswer:function t(){var e=this;return(0,a.default)(s.default.mark(function t(){var n,r,a,i;return s.default.wrap(function t(s){while(1){switch(s.prev=s.next){case 0:e.uploadData={student_answer_list:[],student_paper_contact_id:e.currentConcatId,course_id:e.$store.state.currentCourseId};for(n in e.totalQuestion){r=u(e.totalQuestion[n]);try{for(r.s();!(a=r.n()).done;){i=a.value;e.uploadData.student_answer_list.push({id:i.student_answer_id,score:parseInt(i.student_score)})}}catch(t){r.e(t)}finally{r.f()}}e.$http.post("/course/teacher_correct_paper/",e.uploadData).then(function(t){if(t.code===200){e.$bkMessage({message:"批改成功",theme:"success"});e.$http.get("/course/get_student_answer_info/",{params:{course_id:e.$store.state.currentCourseId,paper_id:e.currentPaperId}}).then(function(t){e.notSubmittedStudentList=t.data.not_submitted;if((new Date).getTime()>e.currentPaperEndTime){e.studentInfoList=t.data.submitted.filter(function(t){return t.status==="SUBMITTED"||t.status==="MARKED"||t.status==="SAVED"})}else{e.studentInfoList=t.data.submitted.filter(function(t){return t.status==="SUBMITTED"||t.status==="MARKED"})}e.studentInfo=e.studentInfoList[e.currentStudentIndex]})}});e.toTop();case 4:case"end":return s.stop()}}},t)}))()},toNextStudent:function t(){var e=this;return(0,a.default)(s.default.mark(function t(){return s.default.wrap(function t(n){while(1){switch(n.prev=n.next){case 0:if(e.currentStudentIndex+1>=e.studentInfoList.length){e.$bkMessage({message:"已经是最后一个学生啦！",theme:"warning"})}else{e.currentStudentIndex++;e.studentInfo=e.studentInfoList[e.currentStudentIndex];e.getStudentQuestionStation();e.toTop()}case 1:case"end":return n.stop()}}},t)}))()},toPreStudent:function t(){var e=this;return(0,a.default)(s.default.mark(function t(){return s.default.wrap(function t(n){while(1){switch(n.prev=n.next){case 0:if(e.currentStudentIndex-1<0){e.$bkMessage({message:"前面没有学生啦！",theme:"warning"})}else{e.currentStudentIndex--;e.studentInfo=e.studentInfoList[e.currentStudentIndex];e.getStudentQuestionStation();e.toTop()}case 1:case"end":return n.stop()}}},t)}))()},chooseStudent:function t(e){var n=this;return(0,a.default)(s.default.mark(function t(){return s.default.wrap(function t(r){while(1){switch(r.prev=r.next){case 0:n.currentStudentIndex=e;n.studentInfo=n.studentInfoList[n.currentStudentIndex];n.getStudentQuestionStation();n.toTop();n.gradeCard.visible=false;case 5:case"end":return r.stop()}}},t)}))()},toTop:function t(){this.$refs.top.scrollTop=0}}};e.default=d},108:function(t,e,n){},163:function(t,e,n){"use strict";var r=n(108);var s=n.n(r);var a=s.a},187:function(t,e,n){"use strict";var r=function(){var t=this;var e=t.$createElement;var n=t._self._c||e;return t.paperEmpty?n("div",{staticClass:"wrapper"},[n("bk-exception",{attrs:{type:"empty",scene:"page"}},[t._v("暂未要批改的试卷")])],1):n("div",{ref:"top",staticClass:"wrapper"},[n("div",{staticClass:"header"},[n("h2",[t._v("试卷信息")]),t._v(" "),n("bk-tag",{attrs:{theme:t.studentInfo.status==="MARKED"?"success":"danger",radius:"10px",type:"filled"}},[t._v(t._s(t.studentInfo.status==="MARKED"?"已批改":"未批改"))])],1),t._v(" "),n("div",{staticClass:"studentInfo"},[n("span",[t._v("学生班级："+t._s(t.studentInfo.class===null?"未认证班级":t.studentInfo.class))]),t._v(" "),n("span",[t._v("学生姓名："+t._s(t.studentInfo.name===null?"未认证姓名":t.studentInfo.name))]),t._v(" "),n("span",[t._v("学生学号："+t._s(t.studentInfo.class_number))]),t._v(" "),n("span",[t._v("当前分数："+t._s(t.totalScore))])]),t._v(" "),t._l(t.totalQuestion,function(e,r){return n("div",{key:r},[e.length!==0?n("div",[n("h3",[t._v(t._s(r))]),t._v(" "),t._l(e,function(r,s){return n("bk-card",{key:s,staticClass:"radio-common",attrs:{title:s+1+"."+r.question+" （"+r.score+"分）",border:false}},[r.types==="SINGLE"?n("bk-radio-group",{staticClass:"radio-common",model:{value:r.student_answer,callback:function(e){t.$set(r,"student_answer",e)},expression:"childItem.student_answer"}},[n("bk-radio",{attrs:{value:"A",disabled:true}},[t._v("\n                        A："+t._s(r.option_A)+"\n                    ")]),t._v(" "),n("bk-radio",{attrs:{value:"B",disabled:true}},[t._v("\n                        B："+t._s(r.option_B)+"\n                    ")]),t._v(" "),n("bk-radio",{attrs:{value:"C",disabled:true}},[t._v("\n                        C："+t._s(r.option_C)+"\n                    ")]),t._v(" "),n("bk-radio",{attrs:{value:"D",disabled:true}},[t._v("\n                        D："+t._s(r.option_D)+"\n                    ")])],1):t._e(),t._v(" "),r.types==="MULTIPLE"?n("bk-checkbox-group",{staticClass:"radio-common",model:{value:r.student_answer,callback:function(e){t.$set(r,"student_answer",e)},expression:"childItem.student_answer"}},[n("bk-checkbox",{attrs:{value:"A",disabled:true}},[t._v("\n                        A："+t._s(r.option_A)+"\n                    ")]),t._v(" "),n("bk-checkbox",{attrs:{value:"B",disabled:true}},[t._v("\n                        B："+t._s(r.option_B)+"\n                    ")]),t._v(" "),n("bk-checkbox",{attrs:{value:"C",disabled:true}},[t._v("\n                        C："+t._s(r.option_C)+"\n                    ")]),t._v(" "),n("bk-checkbox",{attrs:{value:"D",disabled:true}},[t._v("\n                        D："+t._s(r.option_D)+"\n                    ")]),t._v(" "),n("bk-checkbox",{attrs:{value:"E",disabled:true}},[t._v("\n                        E："+t._s(r.option_E)+"\n                    ")])],1):t._e(),t._v(" "),n("div",{staticStyle:{"margin-top":"10px"}},[t._v("\n                    学生答案："),n("span",[t._v(t._s(r.student_answer))])]),t._v(" "),n("div",{staticStyle:{"margin-top":"10px"}},[t._v("\n                    正确答案为：\n                    "),r.types==="JUDGE"?n("span",[t._v(t._s(e.answer==="false"?"F":"T"))]):n("span",[t._v(t._s(r.answer))])]),t._v(" "),n("div",{staticStyle:{"margin-top":"10px"}},[t._v("\n                    打分："),n("bk-input",{staticStyle:{width:"110px"},attrs:{type:"number",max:r.score,min:0},model:{value:r.student_score,callback:function(e){t.$set(r,"student_score",e)},expression:"childItem.student_score"}})],1)],1)})],2):t._e()])}),t._v(" "),n("bk-button",{staticStyle:{width:"120px",position:"fixed",bottom:"220px",right:"6%","border-radius":"20px"},attrs:{theme:"primary",type:"submit"},on:{click:t.toPreStudent}},[t._v("上一个")]),t._v(" "),n("bk-button",{staticStyle:{width:"120px",position:"fixed",bottom:"170px",right:"6%","border-radius":"20px"},attrs:{theme:"primary",type:"submit"},on:{click:t.toNextStudent}},[t._v("下一个")]),t._v(" "),n("bk-button",{staticStyle:{width:"120px",position:"fixed",bottom:"120px",right:"6%","border-radius":"20px"},attrs:{theme:t.studentInfo.status==="MARKED"?"warning":"success",type:"submit"},on:{click:t.checkAnswer}},[t._v(t._s(t.studentInfo.status==="MARKED"?"重新批改":"确认批改"))]),t._v(" "),n("bk-button",{staticStyle:{width:"120px",position:"fixed",bottom:"270px",right:"6%","border-radius":"20px"},attrs:{theme:"success",outline:true},on:{click:function(e){t.gradeCard.visible=true}}},[t._v("\n        展开批改情况\n    ")]),t._v(" "),n("bk-dialog",{attrs:{width:"720",position:t.gradeCard.position,title:"批改卡","show-footer":false},model:{value:t.gradeCard.visible,callback:function(e){t.$set(t.gradeCard,"visible",e)},expression:"gradeCard.visible"}},[n("div",{staticClass:"gradeCardContent"},[n("h3",[t._v("已提交")]),t._v(" "),n("div",{staticStyle:{display:"flex","flex-wrap":"wrap"}},t._l(t.studentInfoList,function(e,r){return n("div",{key:e.student_id},[n("bk-button",{staticStyle:{"margin-left":"10px","margin-bottom":"10px",width:"110px",height:"40px","font-size":"18px","border-radius":"5px",overflow:"hidden","text-overflow":"ellipsis"},attrs:{theme:e.status==="MARKED"?"success":"default"},on:{click:function(e){t.chooseStudent(r)}}},[t._v(t._s(e.name===null?e.student_id:e.name))])],1)}),0),t._v(" "),n("h3",[t._v("未提交")]),t._v(" "),n("div",{staticStyle:{display:"flex","flex-wrap":"wrap"}},t._l(t.notSubmittedStudentList,function(e){return n("div",{key:e.student_id},[n("bk-button",{staticStyle:{"margin-left":"10px","margin-bottom":"10px",width:"110px",height:"40px","font-size":"18px","border-radius":"5px",overflow:"hidden","text-overflow":"ellipsis"},attrs:{theme:"danger",disabled:""}},[t._v(t._s(e.name===null?e.student_id:e.name))])],1)}),0)])])],2)};var s=[];n.d(e,"a",function(){return r});n.d(e,"b",function(){return s})},80:function(t,e,n){"use strict";n.r(e);var r=n(187);var s=n(106);for(var a in s)if(a!=="default")(function(t){n.d(e,t,function(){return s[t]})})(a);var u=n(163);var i=n(2);var o=Object(i["a"])(s["default"],r["a"],r["b"],false,null,"376583bc",null);e["default"]=o.exports}}]);