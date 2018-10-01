$(document).ready(function(){
  $("#img_room").mouseover(function(){
     $("#img_room").css({
         "opacity": 0.5
     });
  });
  $("#img_room").mouseout(function(){
     $("#img_room").css({
         "opacity": 1
     });
  });
  $("#img_kitchen").mouseover(function(){
     $("#img_kitchen").css({
         "opacity": 0.5
     });
  });
  $("#img_kitchen").mouseout(function(){
     $("#img_kitchen").css({
         "opacity": 1
     });
  });
});