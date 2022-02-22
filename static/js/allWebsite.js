$(document).ready(function(){
  function launchPermissionModal(permissionData){
    $("#LibraryPermissionModal").modal("show")
    $.ajax({
      type: "GET",
      url: "/ajax_get_library_permissions/",
      data: {permission_data: permissionData},
      datatype: "json",
      success: function(json){
        console.log(json)
        if ("id" in json){
          console.log("There are permissions");
          $("#activateLibraryPermissions").hide()
        } else {
          console.log("There are nbo permissions")
          $("#activateLibraryPermissions").show()
          
        }
      }
    })
  }

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

function highlightModNavLink(linkName){
  $("[name='modLink']").removeClass("active");
  $(linkName).addClass("active");
}
$(document).on("click", "button[name='libraryPermissionModalLaunch']", function(e){
  let permissionData = $(this).val()
  launchPermissionModal(permissionData);
})
})
