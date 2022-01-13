$(document).ready(function(){
  $("#selectRootOrgnaisation").click();
  loadMembersList();
});
$("#id_parent_organisation").on('change', function(){
  loadMembersList();
});
// Upon selecting an organisation request all the details of it.
$("button[name='suborganisationSelect']").click(function(){
  let orgId = $(this).val();
  $("#selectedSubOrg").val(orgId);
  $.ajax({
    type : "GET",
    url : "/get_organisation_data/",
    data: { organisation_id: orgId, },
    datatype: 'json',
    success: function(json){
      console.log(json)
      let members = json.org_members;
      let pathways = json.group_pathways;
      let membersIds = [];

// Add members data to column
      if(members.length === 0){
        $("#membersList").empty();
        $("#membersList").append(
          `<li class="list-group-item">
            No members added yet
          </li>`)
      } else {
      $("#membersList").empty();
      $.each(members, function(index, member){
        membersIds.push(member.member.id);

        $("#membersList").append(
          `<li class="list-group-item">
            <a type="button" name="memberInfoTrigger" value="${member.id}">
            ${member.member.username}: ${member.member.first_name} ${member.member.last_name}
            </a>
          </li>`)
      });
    };
// add pathways data to pathway column
      $("#pathwayList").empty();
      $.each(pathways, function(index, pathway){
        console.log(pathway.pathway.title);
        $("#pathwayList").append(`
          <li class="list-group-item ">
            <a type="button" name="pathwayInfoTrigger" value="${pathway.pathway.id}">
              ${pathway.pathway.title}
            </a>
        </li>`)
      });
// Load members from parent organisation to add members box only if they are not a member
// of the focused organisation
      if (json.parent_organisation){
        let parentOrganisationMembers = json.parent_organisation.org_members;
        $("#addMemberFromParent").empty();
        $.each(parentOrganisationMembers, function(index, member){
          if (membersIds.includes(member.member.id) ){
            console.log("Already in group")
          } else {
            $("#addMemberFromParent").append(`
              <li class="list-group-item">
                <div class="form-check">
                <input class="form-check-input" name="updatemembers" type="checkbox" value="${member.member.id}" id="newMemberCheck_${member.member.id}">
                <label class="form-check-label" for="newMemberCheck_${member.member.id}">
                  ${member.member.username}: ${member.member.first_name} ${member.member.last_name}
                </label>
                </div>

              </li>`)
          };
        });
        $("#addMemberFromParent").append(`
          <button name="add_members_to_org_by_id" value="${orgId}" class="btn btn-al w-100 my-2">Add selected</button>
          <button class="btn btn-al w-100 my-2">Cancel & close</button>`);
      } else{
// If a root organisation display invite information
        $("#addMemberFromParent").empty();
        $("#addMemberFromParent").append(`
          <li class="list-group-item">
            You have selected a root organisation, new members will have to accept your invite, search for new members above.
          </li>`);
      };



    }});
});


function loadMembersList() {
  $("#parentMembers").empty();
  $("#parentMembers").append(`<div class="spinner-border text-primary text-center" role="status">
  <span class="visually-hidden">Loading...</span>
</div`)
  let parentId = $("#id_parent_organisation").val();
  console.log(parentId);
  $.ajax({
    type: "GET",
    url: "/get_organisation_members/",
    data: {"organisation_id": parentId,},
    datatype:"json",
    success: function(json){
      $("#parentMembers").empty();
      $.each(json, function(index,member){
        $("#parentMembers").append(`
          <li class="list-group-item">
          <div class="form-check">
          <input class="form-check-input" name="members" type="checkbox" value="${member.id}" id="newMemberCheck_${member.id}">
          <label class="form-check-label" for="newMemberCheck_${member.id}">
            ${member.username}: ${member.first_name} ${member.last_name}
          </label>
        </div>
      </li>`)
      });

}}
)};



$("#userSearchInput").keyup(function(){
  let searchPhrase = $("#userSearchInput").val()
  let subOrgId = $("#selectedSubOrg").val()
  console.log($("#userSearchInput").val());
  $.ajax({
      method: "GET",
      url: "/ajax_search_exact_user/",
      data: {"search_phrase": searchPhrase,
            "selected_organisation":subOrgId },
      datatype:"json",
      success: function(data){
        console.log(data);
        $("#userSearchResults").empty();
        if(data.user){
          $("#userSearchResults").append(`
            <li class="list-group-item">
            ${data.user.username}: ${data.user.first_name} ${data.user.last_name}
            <p><small>Selected: <span id="selectedStatus">${data.status.selected}</span><br>
            <span id="rootStatus">${data.status.root}</span></small></p>
            </li>`);
            if(data.status.root === null){
              $('#rootStatus').empty();
              $('#rootStatus').append('<a href="#">Invite to root organisation</a>')
            } else {
              if(data.status.selected === null){
                $('#selectedStatus').empty();
                $('#selectedStatus').append('<a href="#">Add to suborganisation</a>')
              }
            };
        } else {
          $("#userSearchResults").append(`
            <li class="list-group-item">
            No results found
            </li>`);
        };

      }});
});
