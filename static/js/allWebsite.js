$(document).ready(function(){
  function launchPermissionModal(permissionData){
    $("#LibraryPermissionModal").modal("show")
    $("button[name='activateLibraryPermission']").val(permissionData)
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
          $("#currentLibraryPermissions").show()
          $("#canBeViewedInLibrary").text(json.can_be_viewed_in_library)
          $("#canBeUsedInLibrary").text(json.can_be_used)
          $("#authorVisibilityHidden").text(json.author_visibility_hidden)
          $("#LibraryPermissionId").val(json.id)
        } else {
          console.log("There are no permissions")
          $("#activateLibraryPermissions").show()
          $("#currentLibraryPermissions").hide()

        }
      }
    })
  }
  function libraryPermissionModalHideAndReset(){
      $("#LibraryPermissionModal").modal("hide")
      $("#editCurrentLibraryPermissions").hide()
  }
  function submitNewLibraryPermission(permissionData){
    $.ajax({
      type: "POST",
      url: "/ajax_edit_library_permissions/",
      data: {
            permission_data: permissionData,
            can_be_viewed_in_library: $("#id_can_be_viewed_in_library").is(':checked'),
            can_be_used: $("#id_can_be_used").is(':checked'),
            author_visibility_hidden: $("#id_author_visibility_hidden").is(':checked'),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),

            }

    })
  }
  function submitEditLibraryPermission(){
    $.ajax({
      type: "POST",
      url: "/ajax_edit_library_permissions/",
      data: {
            permission_id: $("#LibraryPermissionId").val(),
            can_be_viewed_in_library: $("#id_edit_can_be_viewed_in_library").is(':checked'),
            can_be_used: $("#id_edit_can_be_used").is(':checked'),
            author_visibility_hidden: $("#id_edit_author_visibility_hidden").is(':checked'),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
          },
      success: function(json){
        if (json.error){
          console.log("We couldn't proceed")
        } else {
          libraryPermissionModalHideAndReset()

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
  function submitVote(contentData, isVoteUp){
    $.ajax({
      type: "POST",
      url: "/Vote_ajax_submit/",
      datatype: "json",
      data: { content_data: contentData,
              is_vote_up: isVoteUp,
              csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            }
    })
  }
  $(document).on("click", "button[name='libraryPermissionModalLaunch']", function(e){
    let permissionData = $(this).val()
    launchPermissionModal(permissionData);
  })
  $(document).on("click", "button[name='activateLibraryPermission']", function(e){
    e.preventDefault()
    let permissionData = $(this).val()
    submitNewLibraryPermission(permissionData)
  })
  $(document).on("click", "button[id='editCurrentPermissionsLaunch']", function(e){
    e.preventDefault()
    console.log("hello")
    $("#editCurrentLibraryPermissions").show()
  })
  $(document).on("click", "button[name='closeEditCurrentPermissionsLaunch']", function(e){
    e.preventDefault()
    $("#editCurrentLibraryPermissions").hide()
  })
  $(document).on("click", "button[name='submitEditLibraryPermission']", function(e){
    submitEditLibraryPermission()
  })
  $(document).on("click", "button[name='submitVoteUp']", function(e){
    e.preventDefault()
    console.log("registered click")
    let contentData = $(this).val()
    submitVote(contentData, true)
  })
  $(document).on("click", "button[name='submitVoteDown']", function(e){
      e.preventDefault()
    console.log("registered click")
    let contentData = $(this).val()
    submitVote(contentData, false)
  })

})
