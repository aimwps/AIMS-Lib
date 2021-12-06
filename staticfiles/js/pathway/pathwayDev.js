$(document).ready(function () {
  getPathwayData() ;

  // $('#contentSettingModal').on('show.bs.modal', function(e) {
  //
  //     //get data-id attribute of the clicked element
  //     var contentId = $(e.relatedTarget).data('content-id');
  //     var contentData = $.getValues("/get_dev_pathway_content/");
  //     //populate the textbox
  //     $(e.currentTarget).find('input[name="contentId"]').val(contentId);
  });

// $(document).on("click", "")

function getPathwayData(){
  $.ajax({type: "GET",
          url:  "/get_dev_pathway_content/",
          data: {
                  pathway: $("input[name=pathway_id]").val(),
                },
          datatype: 'json',
          success: function(data){
            var json = JSON.parse(data);
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
                        <button onClick="editContentInModal(${item.id})" class="btn btn-sm btn-al" data-bs-toggle="modal" data-bs-target="#contentSettingModal"><i class="fas fa-list-ul"></i></button>
                        </div>
                        <div class="col-9 me-auto">
                          Completion rules
                        </div>
                      </div>
                      <div class="row my-2">
                        <div class="col-3 ms-auto">
                        <button onClick="deletePathwayContent(${item.id})" class="btn btn-sm btn-al" data-bs-toggle="modal" data-bs-target="#contentDeleteModal"><i class="far fa-trash-alt"></i></button>
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
                  <a class="btn btn-sm btn-al" onClick="editContent(${item.id}, 'move-up')"><i class="fas fa-chevron-up"></i></a>
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
                  <a type="button" class="btn btn-sm btn-al" onClick="editContent(${item.id},'move-down')"><i class="fas fa-chevron-down"></i></a>
                  </div>
                  <div class="col-9 me-auto">
                    Move this down in order
                  </div>
                  </div>`)
              };
              if (item.content_type =="video"){
                console.log("vid", item.video.title)
                $("#contentTitle"+index).append(`${item.video.title}`)
              } else if(item.content_type =="article"){
                $("#contentTitle"+index).append(`${item.article.title}`)
              } else if(item.content_type =="benchmark"){
                $("#contentTitle"+index).append(`${item.benchmark.title}`)
              } else {
                $("#contentTitle"+index).append("unknown file")
              };

            })
          }})
};

function editContent(contentId, actionType){
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
        success: function(data){
          var json = JSON.parse(data);
          console.log("json", json);
          console.log("anytime", json.pathway_obj.complete_anytime_overide);
          console.log("move on", json.pathway_obj.complete_to_move_on)
          // populate the form with data
          $('#id_complete_anytime_overide').prop('checked', json.pathway_obj.complete_anytime_overide);
          $('#id_complete_to_move_on').prop('checked', json.pathway_obj.complete_to_move_on);
          $('#id_revise_frequency').val(json.pathway_obj.revise_frequency);
          $('#contentObjId').val(json.pathway_obj.id);
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
function ajax_submit_delete_pathway_content(){
  $.ajax({type:"POST",
          url:"/ajax_submit_delete_pathway_content/",
          data: {csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                content_id: $("#contentObjId").val(),
                type: 'delete',},
          success: function(){
            $('#contentDeleteModal').modal('toggle');
            getPathwayData();
          }
              })
}
