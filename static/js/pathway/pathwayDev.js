$(document).ready(function () {
  getPathwayData() ;
  $('#contentSettingModal').on('show.bs.modal', function(e) {

      //get data-id attribute of the clicked element
      var contentId = $(e.relatedTarget).data('content-id');
      var contentData = $.getValues("/get_dev_pathway_content/");
      //populate the textbox
      $(e.currentTarget).find('input[name="contentId"]').val(contentId);
  });
});

$(document).on("click", "")

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
                        <button data-content-id="${item.id}" class="btn btn-sm btn-al" data-bs-toggle="modal" data-bs-target="#contentSettingModal"><i class="fas fa-gavel"></i></button>
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

function editContent(contentID, actionType){
  $.ajax({type:"POST",
          url:"/dev_pathway_edit/",
          data:{content_id: contentID,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action_type: actionType},
              success: function(){
                getPathwayData();
              }})
};

$.extend({
    getValues: function(url) {
        var result = null;
        $.ajax({
            url: url,
            type: 'get',
            dataType: 'xml',
            async: false,
            success: function(data) {
                result = data;
            }
        });
       return result;
    }
});
