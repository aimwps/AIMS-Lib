$(document).ready(function(){
  function ajaxFillPathwayModal(pathId){
    $.ajax({
        type:"GET",
        url: "/ajax_get_organisation_pathway_data",
        data: { pathway: pathId,
                organisation: $("#selectedSubOrg").val()},
        datatype:"json",
        success: function(json){
          console.log("this json we want",json)
          console.log("also this length", json.active_members.length)
          $("#pathwayModalLabel").text(json.pathway.title);
          $("#pathwayModalDescription").text(json.pathway.description);
          $("#inOrgSubscribers").text(json.branch_members)
          $("#activePathwayInvites").text(json.active_members.length)
          $("#pendingPathwayInvites").text(json.pending_members.length)
          $("#externalPathwayMembership").text(json.own_subscription_members.length)
          $("#unspentOrgPathwayInvites").text(json.pathway_available_invites)
          $("#noPathwayInviteMembers").text(json.without_pathway_invite.length)
          $("#pathwayInviteId").val(json.pathway.id)

          // List active members in display
          $("#activePathwayMembers").empty()
          $.each(json.active_members, function(idx, member){
            console.log(member)
            $("#activePathwayMembers").append(`
              <li class="list-group-item">
                ${member.member.username}: ${member.member.first_name} ${member.member.last_name}
                </li>
              `)

          });

          // Add members without invite to invite form.
          $("#orgMembersToInvite").empty()
          $.each(json.without_pathway_invite, function(idx, member){
            $("#orgMembersToInvite").append(`
              <li class="list-group-item">
              <div class="form-check">
              <input class="form-check-input" name="members" type="checkbox" value="${member.member.id}" id="newMemberCheck_${member.id}">
              <label class="form-check-label" for="newMemberCheck_${member.member.id}">
                ${member.member.username}: ${member.member.first_name} ${member.member.last_name}
              </label>
            </div>
          </li>`)
          })

          // Add members with pending invite to displa
          $("#orgMembersPendingInvite").empty()
          $.each(json.pending_members, function(idx, member){
            $("#orgMembersPendingInvite").append(`
              <li class="list-group-item">
                ${member.member.username}: ${member.member.first_name} ${member.member.last_name}
                </li>
              `)
          })

          // Add organisation members with external invite to
          $("#orgMembersExternalInvite").empty();
          $.each(json.own_subscription_members, function(idx, member){
            $("#orgMembersExternalInvite").append(`
              <li class="list-group-item">
                ${member.member.username}: ${member.member.first_name} ${member.member.last_name}
                </li>
              `)
          })


          // Add the pathway costs and buy buttons to the collapse frame
          $("#purchaseInviteCosts").empty()
          $.each(json.pathway_costs, function(idx, cost){
          let plural = (idx === 0) ? `Single pathway invite: £${cost.purchase_cost}`:`${cost.purchase_quantity} invites: £${cost.purchase_cost}`;
          console.log("plural", plural)
          $("#purchaseInviteCosts").append(`
            <li class="list-group-item text-right">
             ${plural}
              <button type="submit" value="${cost.id}" class="btn btn-link" name="org_purchase_pathway_invites">
                <i class="fas fa-shopping-basket"></i>
              </button>
            </li>`)

          });

          // add the pathway contents to the modal display
          $("#pathwayModalContentList").empty()
          $.each(json.pathway.full_pathway, function(idx, content){
            if (content.content_type === "article"){
              $("#pathwayModalContentList").append(`
                <li class="list-group-item">
                  <i class="far fa-newspaper"></i> <a href="/article/${content.article.id}">${content.article.title}</a>
                </li>
                `)
            } else if(content.content_type === "video"){

              $("#pathwayModalContentList").append(`
                <li class="list-group-item">
                   <i class="fas fa-film"></i> <a href="/article/${content.video.id}"> ${content.video.title}</a>
                </li>
                `)
            } else if (content.content_type === "benchmark"){
              $("#pathwayModalContentList").append(`
                <li class="list-group-item">
                   <i class="fas fa-film"></i> <a href="/benchmark/${content.benchmark.id}"> ${content.benchmark.title}</a>
                </li>
                `)
            } else {
              console.log("errrorrs")
            };


    })
  }})}
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
  function submitNewMember(orgId){
      $.ajax({
        method: "POST",
        url: "/ajax_submit_new_membership/",
        data: { organisation_id: orgId,
                user_id: $("#inviteUserById").val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()},
        success: function(){
          $("#userSearchInput").val("");
          $("#addMember").collapse('toggle');
          $("#userSearchResults").empty();
          console.log("success")
        }
      });
  };
  function getUserPathwayData(orgId){
    $.ajax({
      method:"GET",
      url:"/ajax_get_user_and_bookmarked_pathway_data/",
      data: { organisation_id: orgId},
      success: function(data){
        console.log("pathway info",data);
        $("#myPathways").empty();
        $.each(data.created, function(index, userPathway){
          $("#myPathways").append(`
            <li class="list-group-item">
            <div class="form-check">
            <input class="form-check-input" name="addPathways" type="checkbox" value="${userPathway.id}" id="userPathwayCheck_${userPathway.id}">
            <label class="form-check-label" for="userPathwayCheck_${userPathway.id}">
              ${userPathway.title}
            </label>
            </div>

            </li>`)
        })

      }
    })
  };
  function selectOrganisationBranch(orgId){
    getUserPathwayData(orgId);

  // set the organisation ID for adding a pathway to it
    $("button[name='add_pathways_to_organisation']").val(orgId)

  // Set the organisation id for  global access
    $("#selectedSubOrg").val(orgId);

  // retrieve details of the selected organisation section
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
  // display parent group in span
        $("#parentOrgTitle").empty()
        if (json.parent_organisation){
          $("#parentOrgTitle").append(`Add from: ${json.parent_organisation.title}`)
        }else {
          $("#parentOrgTitle").append(`Invite only`)
        };


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
          if(member.status==="active"){
          $("#membersList").append(
            `<li class="list-group-item">
              <a type="button" name="memberInfoTrigger" value="${member.member.id}">
              ${member.member.username}: ${member.member.first_name} ${member.member.last_name}
              </a>
            </li>`)};
        });
      };
  // add pathways data to pathway column
        $("#pathwayList").empty();
        $.each(pathways, function(index, pathway){
          $("#pathwayList").append(`
            <li class="list-group-item ">
              <button class="btn btn-link w-100 text-start nounderline" type="button" name="pathwayInfoTrigger" value="${pathway.pathway.id}">
                ${pathway.pathway.title}
              </button>
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
            `);
        } else {
  // If a root organisation display invite information
          $("#addMemberFromParent").empty();
          $("#addMemberFromParent").append(`
            <li class="list-group-item">
              You have selected a root organisation, new members will have to accept your invite, search for new members above.
            </li>`);
        };



      }});
  };

  $("#selectRootOrgnaisation").click();
  $("#id_parent_organisation").on('change', function(){
    loadMembersList();
  });
  // Upon selecting an organisation request all the details of it.
  $("button[name='suborganisationSelect']").click(function(){
    $("button[name='suborganisationSelect']").css("background-color", "white")
    $(this).css("background-color", "#f9944b");
    let orgId = $(this).val();
    selectOrganisationBranch(orgId)
  })

    // Function used to display user created and bookmarked pathways in add pathway area
  $("#userSearchInput").keyup(function(){
    let searchPhrase = $("#userSearchInput").val()
    let subOrgId = $("#selectedSubOrg").val()
    console.log($("#userSearchInput").val());
    $.ajax({
        method: "GET",
        url: "/ajax_search_exact_user/",
        data: {search_phrase: searchPhrase,
              selected_organisation:subOrgId },
        datatype:"json",
        success: function(data){
          console.log(data);
          $("#userSearchResults").empty();
          if(data.user){
            $("#userSearchResults").append(`
              <li class="list-group-item">
              ${data.user.username}: ${data.user.first_name} ${data.user.last_name}
              <p><small>
              <span id="rootStatus">${data.status.organisation.title}: ${data.status.status}</span>
              </small></p>
              </li>`);
              if (data.status.status === "no membership"){
                $("#userSearchResults").append(`
                    <input type="hidden" name="inviteUserById" id="inviteUserById" value="${data.user.id}">
                    <button type="button" name="submitInvite" id="submitInvite" value="${data.status.organisation.id}" class="btn btn-al w-100"> Send Invite</button>
    `);
              }
          } else {
            $("#userSearchResults").append(`
              <li class="list-group-item">
              No results found
              </li>`);
          };

        }});
  });
  $("button[name='cancelCloseMember']").click(function(){
    $("#userSearchInput").val("");
    $("#addMember").collapse('toggle');
    $("#userSearchResults").empty();
  });
  $("button[name='cancelCloseOrgs']").click(function(){
    $("input[name='title']").val("");
    $("#addOrganisation").collapse('toggle');
  });
  $("button[name='cancelClosePathways']").click(function(){
    $("#userSearchInput").val("");
    $("#addPathway").collapse('toggle');

  });
  $(document).on("click", "#submitInvite", function(){
    let orgId = $(this).val();
    submitNewMember(orgId)
  })
  $(document).on("change", "#selectOrganisationBranch", function(){
    let orgId = $(this).val();
    selectOrganisationBranch(orgId);
  });
  $(document).on("click", "[name='pathwayInfoTrigger']", function(){
    let pathId = $(this).val();
    $("#pathwayModal").modal("show")
    console.log("thisisPATHID",pathId)
    ajaxFillPathwayModal(pathId)

  });
  // $(document).on("click", "#buyInviteBtn", function(){
  //   $("#purchaseInvitesModal").modal("show")
  // })
  loadMembersList();
});
