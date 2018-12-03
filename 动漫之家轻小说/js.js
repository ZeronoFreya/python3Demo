// ==UserScript==
// @name     动漫之家[轻小说]
// @version  1
// @include  http://q.dmzj.com/*
// @exclude  http://q.dmzj.com/
// @grant    none
// @require  http://code.jquery.com/jquery-2.1.1.min.js
// ==/UserScript==

$(function(){
  var maxIdx = 0;

	$("body").css({"width": "320px","margin":"0 auto"});
  var toolBar = $("<div></div>");
  toolBar.css({
  	"position":"fixed",
    "top":"0",
    "left":"0",
    "height":"100%",
    "width":"100px",
    "padding":"100px 10px",
    "background":"rgba(0,0,0,.5)"
  })
  var btncss = {
  	"display":"block",
    "width":"100%",
    "height":"30px",
    "margin-bottom":"10px"
  };
  var download = $("<button type='button'>全部下载</button>");
  download.css(btncss)
  toolBar.append(download);
  var downloadFrom = $("<button type='button'>从...下载</button>");
  downloadFrom.css(btncss);
  toolBar.append(downloadFrom);
  downloadFrom.on("click",function(){
    var _i = Number( prompt("从哪里开始下载？","1") );
    if (_i <= maxIdx){
      var title = prompt( "书名：",$("div.con h3").text() );
      if(title){
        var list = [];
        $("#sort_div_p .chapname").each(function(i, v){
          if(i>=_i) {
            list.push({
                   "url" : $(this).find("a").attr("href"),
                 "title" : title,
              "subtitle" : $(this).find(".chapnamesub").text()
            });
          }
        })
      }

      //console.log(JSON.stringify(list, null, 4));
      var outdiv = $("<div></div>");
      outdiv.css({
      	"position":"fixed",
        "top":"50%",
        "left":"50%",
        "transform":"translate(-50%, -50%)",
        "z-index":"9999"
      });
      var textarea = $("<textarea></textarea>");
      textarea.css({
        "padding":"30px",
      	"background":"#0c0c0d",
        "width":"500px",
        "height":"500px",
        "max-width":"80vw",
        "max-height":"80vh",
        "overflow":"auto",
        "font-size":"16px",
        "color":"#FF4857"
      });
      textarea.text( JSON.stringify(list, null, 4) );
      var closeBtn = $("<button type='button'>X</button>");
      closeBtn.css({
      	"position": "absolute",
        "right": "0",
        "top": "0"
      });
      closeBtn.on("click",function(){
      	outdiv.remove();
      });
      outdiv.append(textarea);
      outdiv.append(closeBtn);

      $("html").append(outdiv);
    }else{
    	alert("无效输入！");
    }
  })


  $("html").append(toolBar).css({
  	"padding":"0 100px",
    "background":"#EEE"
  });
  var _i;
  $("#sort_div_p .chapname").each(function(i, v){
    maxIdx = i;
    $(this).css("position","relative");
    _i = $("<i>"+i+"</i>").css({
      "display": "block",
      "position": "absolute",
      "left": "-30px",
      "text-align": "right",
      "width": "25px"
    });
  	$(this).prepend(_i);
  })
})
