$(document).ready(function(){

  let viewTimer = setInterval(countSeconds, 1000);

  function countSeconds(){
    let current = parseInt($("#id_completion_time").val());
    $("#id_completion_time").val(current+1)
    console.log($("#id_completion_time").val())
  }

  $(document).on('click', "[name='submitVideoSession']", function(){
    $("#id_status").val($(this).val());
  })
})
