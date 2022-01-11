$("button[name='suborganisationSelect']").click(function(){
  let orgId = $(this).val();
  $.ajax({
    type : "GET",
    url : "/get_organisation_data/",
    data: { organisation_id: orgId, },
    datatype: 'json',
    success: function(json){
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
