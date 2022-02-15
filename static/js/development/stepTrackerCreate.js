$(document).ready(function(){

  function loadStepTrackerItemToModal(tracker, isABookmark){
    console.log(tracker)
    bookmarkOrDelete(isABookmark)
    $("#viewLibraryStepTrackerResultModal").modal("show")
    $("#submitBookmarkStepTracker").val(tracker.id)
    $("#stepTrackerDetails").empty()
    $("#stepTrackerDetails").append(`
        <li class="list-group-item border-0">
        <small><strong>Tracker: </strong>${tracker.get_tsentence}</small>
          </li>
          <li class="list-group-item border-0">
          <small><strong>Type: </strong>${tracker.get_type_sentence}</small>
            </li>
          <li class="list-group-item border-0">
          <small><strong>Frequency: </strong>${tracker.get_frequency_sentence}</small>
            </li>
          <li class="list-group-item border-0">
          <small><strong>Log window: </strong>A ${tracker.record_log_length}</small>
            </li>`)

  }
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
