

$("#deleteCheck").keyup(function(){
  console.log($("#deleteCheck").val())
  if ($("#deleteCheck").val() === "delete" ){
    $("#deleteCheckSubmit").removeClass();
    $("#deleteCheckSubmit").addClass("btn");
    $("#deleteCheckSubmit").addClass("btn-al");
    $("#deleteCheckSubmit").html("Delete");
  } else {
    $("#deleteCheckSubmit").removeClass();
    $("#deleteCheckSubmit").addClass("btn");
    $("#deleteCheckSubmit").addClass("btn-secondary");
    $("#deleteCheckSubmit").addClass("disabled");
    $("#deleteCheckSubmit").html("type 'delete' to activate");
  }
})
