
$(document).ready(function(){
  var intervalChecker =  setInterval(checkPathwayInvites, 1000);

  function checkPathwayInvites(){
    $.ajax({
      type: "GET",
      url:"/UserPathways_ajax_check_pathway_invites/",
      datatype: 'json',
      success: function(json){
        console.log("paylod", json)
        if (json.length > 0 ){
          $("#inviteArea").show();
          $("#pathwayInvites").empty();
          $.each(json, function(idx, invite){
            $("#pathwayInvites").append(`
              <li class="list-group-item px-0 my-2">
                <a class="nounderline" href="/pathway/${invite.on_pathway.id}"><strong>${invite.on_pathway.title}</strong></a> invite by ${invite.purchase.spent_by_user.username}

                <div class="row m-2">
                <div class="col-6">
                <button type="button" name="submitInviteReject" value="${invite.id}" class="btn btn-sm btn-al w-100"><i class="fas fa-times text-secondary"></i></button>
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
        $("#pathwayInvites").empty();
      };

    }
// Set the sub nav notification
// return the length for main nav notification
    })
  }
  function submitInviteResponse(type, inviteId){
    $.ajax({
      type:"POST",
      url: "/UserPathways_ajax_submit_pathway_invite/",
      data: {
            status: type,
            invite_id: inviteId,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
          },
      datatype: "json",
      success: function(json){
        console.log(json)
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
