$(document).ready(function () {
  getPathwayData() ;
  $("#newPathwayCost").hide()
  function getPathwayCost(){
    $.ajax({type: "GET",
            url:  "/UserPathways_ajax_get_pathway_costs/",
            data: {
                    pathway: $("input[name=pathway_id]").val(),
                  },
            datatype: 'json',
            success: function(json){
              $("#pathwayCostList").empty()
              console.log(json)
              if (json.length > 0) {
              $.each(json, function(idx, cost){
                console.log(cost.purchase_quantity > 1)
                let btnStatus = (json.length > 1 && idx === 0) ? " disabled":" active";
                let plural = (idx === 0) ? `Single user access: £${cost.purchase_cost}`:`${cost.purchase_quantity} units for organisation: £${cost.purchase_cost}`;

                $("#pathwayCostList").append(`
                  <li class="list-group-item">
                    <button type="submit" value="${cost.id}" class="btn btn-link ${btnStatus}" name="delete_pathway_cost">
                      <i class="far fa-trash-alt"></i>
                    </button> ${plural}
                  </li>`)
              });
            } else{
              $("#id_purchase_quantity").val(1);
              $("#id_purchase_quantity").attr("type", "hidden")
              $("#quantity_1").text("1")
              $("#id_pathway").val($("input[name=pathway_id]").val());
              $("#pathwayCostList").append(`
                <li class="list-group-item">This pathway is currently free to join.<br>
                It is visible in the library.<br>
                Add a restriction or cost below.
                </li>`)
            };
          }})
  };
  function getPathwayData(){
    $.ajax({type: "GET",
            url:  "/get_dev_pathway_content/",
            data: {
                    pathway: $("input[name=pathway_id]").val(),
                  },
            datatype: 'json',
            success: function(json){
              // var json = JSON.parse(data);
              console.log(json);
              $("#pathwayContent").empty();
              var pathwayContent = json.pathway_content;
              $.each(pathwayContent, function(index, item){
                console.log("Pathway Content index", index, item);
                $("#pathwayContent").append(`
                  <div class="row py-2 px-0">
                    <div class="col-1">
                    ${item.order_position}
                    </div>
                    <div class="col-4">
                    ${item.content_type}
                    </div>
                    <div class="col-6" id="contentTitle${index}">
                    </div>
                    <div class="col-1">
                      <a class="btn btn-sm btn-al" data-bs-toggle="collapse" href="#contentControls${item.id}" role="button" aria-expanded="false" aria-controls="contentControls${item.id}">
                        <i class="fas fa-cogs"></i>
                      </a>
                    </div>
                    </div>
                    <div class="collapse" id="contentControls${item.id}">
                      <div class="card card-body border-0">
                        <div class="container" id="contentControlsBody${index}">
                        <div class="row my-2">
                          <div class="col-3 ms-auto">
                          <button name="editContentInModalBtn" value="${item.id}"class="btn btn-link" data-bs-toggle="modal" data-bs-target="#contentSettingModal"><i class="fas fa-list-ul"></i></button>
                          </div>
                          <div class="col-9 me-auto">
                            Completion rules
                          </div>
                        </div>
                        <div class="row my-2">
                          <div class="col-3 ms-auto">
                          <button value="${item.id}" name="deletePathwayContentBtn" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#contentDeleteModal"><i class="far fa-trash-alt"></i></button>
                          </div>
                          <div class="col-9 me-auto">
                            Remove content from pathway
                          </div>
                        </div>
                        </div>
                      </div>
                  </div>`);
                if (index != 0){
                  $("#contentControlsBody"+ index).append(`
                    <div class="row my-2">
                    <div class="col-3 ms-auto">
                    <button class="btn btn-link" name="moveContentUp" value="${item.id}""><i class="fas fa-chevron-up"></i></button>
                    </div>
                    <div class="col-9 me-auto">
                      Move this up in order
                    </div>
                    </div>
                    `)
                  };
                if (index+1 != pathwayContent.length ){
                  $("#contentControlsBody"+ index).append(`
                    <div class="row my-2">
                    <div class="col-3 ms-auto">
                    <button class="btn btn-link" name="moveContentDown" value="${item.id}"><i class="fas fa-chevron-down"></i></button>
                    </div>
                    <div class="col-9 me-auto">
                      Move this down in order
                    </div>
                    </div>`)
                };
                if (item.content_type =="Video"){
                  console.log("vid", item.video.title)
                  $("#contentTitle"+index).append(`${item.video.title}`)
                } else if(item.content_type =="Article"){
                  $("#contentTitle"+index).append(`${item.article.title}`)
                } else if(item.content_type =="Benchmark"){
                  $("#contentTitle"+index).append(`${item.benchmark.title}`)
                } else {
                  $("#contentTitle"+index).append("unknown file")
                };

              })
            }})
  };
  function editContent(contentId, actionType){
    console.log("THE CONENT ID TO SUBMMIT", contentId)
    $.ajax({type:"POST",
            url:"/dev_pathway_edit/",
            data:{content_id: contentId,
                  csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                  action_type: actionType},
                success: function(data){
                  var json = JSON.parse(data);
                  getPathwayData();
                  $('#contentControls'+json.pathway_obj).collapse("show");


                }})
  };
  function editContentInModal(contentId){
    $.ajax({type:"GET",
            url:"/ajax_get_pathway_content_obj/",
            data: {content_id:contentId},
          success: function(json){
            console.log("HERE")
            console.log(json)

            // populate the form with data
            $('#id_complete_anytime_overide').prop('checked', json.complete_anytime_overide);
            $('#id_complete_to_move_on').prop('checked', json.complete_to_move_on);
            $('#id_revise_frequency').val(json.revise_frequency);
            $('#contentObjId').val(json.id);
            // getPathwayData();
          }})
  };
  function postUpdateContentSetting(){
      $.ajax({type:"POST",
              url: "/ajax_submit_content_setting_changes/",
              data: {content_id: $('#contentObjId').val(),
                    complete_anytime_overide: $('#id_complete_anytime_overide').is(':checked'),
                    complete_to_move_on: $('#id_complete_to_move_on').is(':checked'),
                    revise_frequency: $('#id_revise_frequency').val(),
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),

                  },
                success:function(){
                      $('#contentSettingModal').modal('toggle');
                      getPathwayData();
                    },

             })
  };
  function deletePathwayContent(contentId){
    $("#contentObjId").val(contentId);
  }
  function ajax_submit_delete_pathway_content(contentId){
    $.ajax({type:"POST",
            url:"/ajax_submit_delete_pathway_content/",
            data: {csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                  content_id: contentId,
                  type: 'delete',},
            success: function(){
              $('#contentDeleteModal').modal('toggle');
              getPathwayData();
            }
                })
  }
  $(document).on("click", "[name='costSettings']", function(e){
    console.log("clicked")
    getPathwayCost()
  });
  $(document).on("click", "#addCostBtn", function(e){
    $("#newPathwayCost").toggle()

})
  $(document).on("click", "[name='add_pathway_cost']", function(){
    $("#id_pathway").val($("input[name=pathway_id]").val())
  })
  $(document).on("click", "#updateContentSetting", function(e){
    postUpdateContentSetting();
  })
  $(document).on("click", "button[name='editContentInModalBtn']", function(e){
    let id = $(this).val();
    console.log("ID", id)
    editContentInModal(id);
  })
  $(document).on("click", "button[name='deletePathwayContentBtn']", function(e){
    let id = $(this).val();
    $("#deleteModalSubmit").val(id)

  })
  $(document).on("click", "button[name='deletePathwayContentBtn']", function(e){
    let id = $(this).val();
    $("#deleteModalSubmit").val(id)

  })
  $(document).on("click", "#deleteModalSubmit", function(e){
    let id = $(this).val();
    ajax_submit_delete_pathway_content(id)

  })
  $(document).on("click", "[name='moveContentDown']", function(e){
    let id = $(this).val()
    console.log("HERE-- DOWN-->", id)
    editContent(id, "move-down")
  } )
  $(document).on("click", "[name='moveContentUp']", function(e){
    let id = $(this).val()
    console.log("HERE- UP--->", id)
    editContent(id, "move-up")
  } )
  });
