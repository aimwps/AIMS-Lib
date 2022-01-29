$(document).ready(function(){

  let viewTimer = setInterval(countSeconds, 1);

  function countSeconds(){
    let current = $("#viewTimer").val();
    $("#viewtimer").val(current+1)
    console.log($("#viewTimer").val())
  }


})
