$("input[name='deleteModalInput']").keyup(function(){
  if ($("input[name='deleteModalInput']").val() === "delete" ){
    $("button[name='deleteModalButton']").removeClass();
    $("button[name='deleteModalButton']").addClass("btn");
    $("button[name='deleteModalButton']").addClass("btn-al");
    $("button[name='deleteModalButton']").html("Delete");
  } else {
    $("button[name='deleteModalButton']").removeClass();
    $("button[name='deleteModalButton']").addClass("btn");
    $("button[name='deleteModalButton']").addClass("btn-secondary");
    $("button[name='deleteModalButton']").addClass("disabled");
    $("button[name='deleteModalButton']").html("type 'delete' to activate");
  }
})
