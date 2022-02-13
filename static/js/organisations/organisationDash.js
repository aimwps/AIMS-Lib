
$(document).ready(function(){
  var intervalChecker =  setInterval(checkOrganisationInvites, 1000);

  function checkOrganisationInvites(){
    $.ajax({
      type: "GET",
      url:"/nav_ajax_check_organisation_invites/",
      datatype: 'json',
      success: function(json){
        if (json.length > 0 ){
          $("#inviteArea").show();
          $("#organisationInvites").empty();
          $.each(json, function(idx, invite){
            $("#organisationInvites").append(`
              <li class="list-group-item px-0 my-2">
                <a class="nounderline" href="/organisation/${invite.organisation.id}"><strong>${invite.organisation.title}</strong></a> invite from ${invite.organisation.author.username}

                <div class="row m-2">
                <div class="col-6">
                <button type="button" name="submitInviteReject"value="${invite.id}" class="btn btn-sm btn-al w-100"><i class="fas fa-times text-secondary"></i></button>
                </div>
                <div class="col-6">
                <button type="button" name="submitInviteAccept" value="${invite.id}" class="btn btn-sm btn-al w-100"><i class="fas fa-check text-primary"></i></button>
                </div>
                </div>


              </li>
          `)
        })
      } else{
        $("#inviteArea").hide();
        $("#organisationInvites").empty();
      };

    }
// Set the sub nav notification
// return the length for main nav notification
    })
  }
  function submitInviteResponse(type, inviteId){
    $.ajax({
      type:"POST",
      url: "/ajax_submit_organisation_invite/",
      data: {
            status: type,
            invite_id: inviteId,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
          },
      datatype: "json",
      success: function(json){
        console.log(json);
        window.location.reload();
      }
    })


  }

$(document).on("click", "[name='submitInviteAccept']", function(){
  submitInviteResponse("active", $(this).val());
});
$(document).on("click", "[name='submitInviteReject']", function(){
  submitInviteResponse("rejected", $(this).val());
});
})
