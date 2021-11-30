$(document).ready(function () {
  getPathwayData() ;
});


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
                  <div class="col-6">
                  ${item.title}
                  </div>
                  <div class="col-1">
                    <a class="btn btn-sm btn-al" data-bs-toggle="collapse" href="#contentControls${index}" role="button" aria-expanded="false" aria-controls="collapseExample">
                      <i class="fas fa-cogs"></i>
                    </a>
                  </div>
                  </div>
                  <div class="collapse" id="contentControls${index}">
                    <div class="card card-body border-0">
                      <div class="container" id="contentControlsBody${index}">
                      <div class="row">
                        <div class="col-3 ms-auto">
                        <a type="button" class="btn btn-sm btn-al"><i class="fas fa-gavel"></i></a>
                        </div>
                        <div class="col-9 me-auto">
                          Completion rules
                        </div>
                      </div>
                      </div>
                    </div>
                  </div>
                </div>`);
              if (index != 0){
                $("#contentControlsBody"+ index).append(`
                  <div class="row my-2">
                  <div class="col-3 ms-auto">
                  <a type="button" class="btn btn-sm btn-al" onClick="editContent(${item.id}, 'move-up')"><i class="fas fa-chevron-up"></i></a>
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

            })
          }})
};

function editContent(contentID, actionType){
  $.ajax({type:"POST",
          url:"/dev_pathway_edit/",
          data:{content_id: contentID,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action_type: actionType},
              success: function(){
                getPathwayData();
              }})
}
