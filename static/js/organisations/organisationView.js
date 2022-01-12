$(document).ready(function(){
  loadMembersList();
});
$("#id_parent_organisation").on('change', function(){
  loadMembersList();
});

$("button[name='suborganisationSelect']").click(function(){
  let orgId = $(this).val();
  $.ajax({
    type : "GET",
    url : "/get_organisation_data/",
    data: { organisation_id: orgId, },
    datatype: 'json',
    success: function(json){
      console.log(json)
      let members = json.members;
      let pathways = json.group_pathways;
      $("#membersList").empty();
      $.each(members, function(index, member){
        $("#membersList").append(
          `<li class="list-group-item">
            <a type="button" name="memberInfoTrigger" value="${member.id}">
            ${member.username}: ${member.first_name} ${member.last_name}
            </a>
          </li>`)
      });
      $("#pathwayList").empty();
      $.each(pathways, function(index, pathway){
        console.log(pathway.pathway.title);
        $("#pathwayList").append(`
          <li class="list-group-item">
            <a type="button" name="pathwayInfoTrigger" value="${pathway.pathway.id}">
              ${pathway.pathway.title}
            </a>
        </li>`)
      });
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
      console.log(json);
      console.log("------------------------------")
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
