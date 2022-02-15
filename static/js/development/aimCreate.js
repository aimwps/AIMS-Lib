$(document).ready(function(){

  function loadAimItemToModal(aimData, isABookmark){
    bookmarkOrDelete(isABookmark)
    console.log(aimData)
    $("#aimBehaviours").empty()
    $("#viewLibraryAimResultModal").modal("show")
    $("#aimTitle").text(aimData.title)
    $("#aimMotivation").text(aimData.motivation)
    $("#submitCopyAim").val(aimData.id)
    $("#submitBookmarkAim").val(aimData.id)
    $.each(aimData.behaviours, function(idx, behaviour){
      $("#aimBehaviours").append(`
        <li class="list-group-item border-0">

          <a class="btn-link nounderline" data-bs-toggle="collapse" href="#behaviourCollapse_${behaviour.id}" role="button" aria-expanded="false" aria-controls="behaviourCollapse_${behaviour.id}">
            ${behaviour.title}
          </a>

            <div class="collapse" id="behaviourCollapse_${behaviour.id}">
              <div class="card card-body border-0">
                <ul class="list-group-flush px-0" id="behaviours_${behaviour.id}_tracker_list">
                </ul>
              </div>
            </div>

        </li>
        `);
        let addToList = `#behaviours_${behaviour.id}_tracker_list`
        if(behaviour.trackers.length > 0){
          $.each(behaviour.trackers, function(tracker_idx, tracker){
            console.log(tracker_idx, tracker)
            $(addToList).append(`
              <li class="list-group-item">
              ${tracker.get_tsentence}
              </li>`)
          });
        }else{
        $(addToList).append(`
          <li class="list-group-item">
         There are no trackers set for this behaviour
          </li>`);

      }

    })
  };
  function bookmarkOrDelete(isABookmark){
    if (isABookmark){
      $("button[name='submitBookmark']").hide()
      $("button[name='deleteBookmark']").show()
    } else {
      $("button[name='submitBookmark']").show()
      $("button[name='deleteBookmark']").hide()
    }
  };

  function loadLibraryItemFromBookmark(id){
    $.ajax({
      method:"GET",
      url: "/LibraryView_ajax_get_bookmark_content/",
      datatype: "json",
      data: {bookmark_id: id},
      success: function(json){
        $("button[name='deleteBookmark']").val(json.id)
        if (json.content_type === "StepTracker"){
          loadStepTrackerItemToModal(json.steptracker, true)
        } else if (json.content_type === "Behaviour"){
          loadBehaviourItemToModal(json.behaviour, true)
        } else if (json.content_type === "Aim"){
          loadAimItemToModal(json.aim, true)
        } else if (json.content_type === "Pathway"){
          loadPathwayItemToModal(json.pathway,true)
        } else if (json.content_type === "Article"){
          loadArticleItemToModal(json.article, true)
        } else if (json.content_type === "VideoLecture"){
          loadVideoItemToModal(json.video, true)
        } else if (json.content_type === "Benchmark"){
          loadBenchmarkItemToModal(json.benchmark, true)
        } else if (json.content_type === "Organisation"){
          loadOrganisationItemToModal(json.benchmark, true)
        } else {
          console.log("content type not recognised")
        }

        }

    });
  }
$(document).on("click", "button[name='loadLibraryItemFromBookmark']", function(e){
  e.preventDefault();
  let id = $(this).val()
  loadLibraryItemFromBookmark(id)
})

$(document).on("change", "#selectBookmark", function(e){
  e.preventDefault()
  let id = $(this).val()
  $("button[name='loadLibraryItemFromBookmark']").val(id)
})
$("#submitCopyAim").hide()
})
