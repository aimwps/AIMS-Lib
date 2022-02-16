$(document).ready(function(){
  function loadVideoItemToModal(videoData, isABookmark){
      bookmarkOrDelete(isABookmark)
      $("#viewLibraryVideoResultModal").modal("show")
      $("#submitBookmarkVideo").val(videoData.id)
      $("[name='addVideoToForm']").val(`${videoData.library_type}_${videoData.id}`)
      $("#videoDetails").empty()
      $("#videoDetails").append(`
        <li class="list-group-item" id="videoItemTitle">
        <small><strong>Title: </strong>${videoData.title}</small>
        </li>
        `)
  }
  function loadArticleItemToModal(articleData, isABookmark){
      bookmarkOrDelete(isABookmark)
      $("#viewLibraryArticleResultModal").modal("show")
      $("#submitBookmarkArticle").val(articleData.id)
      $("[name='addArticleToForm']").val(`${articleData.library_type}_${articleData.id}`)
      $("#articleDetails").empty()
      $("#articleDetails").append(`
        <li class="list-group-item" id="articleItemTitle">
        <small><strong>Title: </strong>${articleData.title}</small>
        </li>
        <li class="list-group-item">
        <small><strong>Description: </strong>${articleData.description}</small>
        </li>
        `)
  }
  function loadBenchmarkItemToModal(benchmarkData, isABookmark){
      bookmarkOrDelete(isABookmark)
      $("#viewLibraryBenchmarkResultModal").modal("show")
      $("#submitBookmarkBenchmark").val(benchmarkData.id)
      $("[name='addBenchmarkToForm']").val(`${benchmarkData.library_type}_${benchmarkData.id}`)
      $("#benchmarkDetails").empty()
      $("#benchmarkDetails").append(`
        <li class="list-group-item" id="benchmarkItemTitle">
        <small><strong>Title: </strong>${benchmarkData.title}</small>
        </li>
        <li class="list-group-item">
        <small><strong>Description: </strong>${benchmarkData.description}</small>
        </li>
        `)
  }
  function bookmarkOrDelete(isABookmark){
    if (isABookmark){
      $("button[name='submitBookmark']").hide()
      $("button[name='deleteBookmark']").hide()
    } else {
      $("button[name='submitBookmark']").hide()
      $("button[name='deleteBookmark']").hide()
    }
    $("#deleteBenchmarkBookmark").hide()
    $("#deleteVideokBookmark").hide()
    $("#deleteArticleBookmark").hide()
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
  function loadLibraryItemToModal(resultData){
        $.ajax({
        type: "GET",
        url: "/LibraryView_ajax_get_library_result/",
        data: {result_phrase: resultData},
        datatype: "json",
        success: function(json){
          console.log(json)
          console.log(json.content.library_type)
          if (json.content.library_type ==="Aim"){
            if (json.bookmark){
              $("button[name='deleteBookmark']").val(json.bookmark.id);
              loadAimItemToModal(json.content, true);
            } else {
              loadAimItemToModal(json.content, false)
            };
          } else if (json.content.library_type === "Behaviour"){
              if (json.bookmark){
                $("button[name='deleteBookmark']").val(json.bookmark.id);
                loadBehaviourItemToModal(json.content, true);
            } else {
                loadBehaviourItemToModal(json.content, false);
            };
          } else if (json.content.library_type === "StepTracker"){
            if (json.bookmark){
              $("button[name='deleteBookmark']").val(json.bookmark.id);
              loadStepTrackerItemToModal(json.content, true);
            } else {
              loadStepTrackerItemToModal(json.content, false);
            };

          } else if (json.content.library_type === "Organisation"){
            if (json.bookmark){
              $("button[name='deleteBookmark']").val(json.bookmark.id);
            loadOrganisationItemToModal(json.content, true);
            } else {
            loadOrganisationItemToModal(json.content, false);
            };


          } else if (json.content.library_type === "Video"){
              if (json.bookmark){
                $("button[name='deleteBookmark']").val(json.bookmark.id);
                loadVideoItemToModal(json.content, true);
              } else {
                loadVideoItemToModal(json.content, false);
              };


          } else if (json.content.library_type === "Article"){
            if (json.bookmark){
                $("button[name='deleteBookmark']").val(json.bookmark.id);
                loadArticleItemToModal(json.content, true);
              } else {
                loadArticleItemToModal(json.content, false);
              };



          } else if (json.content.library_type === "Benchmark"){
            if (json.bookmark){
                $("button[name='deleteBookmark']").val(json.bookmark.id);
                loadBenchmarkItemToModal(json.content, true);
            } else {
                loadBenchmarkItemToModal(json.content, false);
                };

          } else if (json.content.library_type === "Pathway"){
            if (json.bookmark){
                $("button[name='deleteBookmark']").val(json.bookmark.id);
                loadPathwayItemToModal(json.content, true);
            } else {
              loadPathwayItemToModal(json.content, false);
                };
         } else {
            console.log("we haven't uinderstood the contentType")
          };
    }})
  }
  $(document).on("click", "button[name='loadLibraryItemFromBookmark']", function(e){
    e.preventDefault();
    let id = $(this).val()
    loadLibraryItemFromBookmark(id, true)
  })

  $(document).on("click", "button[name='selectBookmark']", function(e){
    e.preventDefault()
    let id = $(this).val()
    loadLibraryItemFromBookmark(id, true)
  })

  $(document).on("click", "button[name='selectArticle']", function(e){
    e.preventDefault();
    let id = $(this).val();
    $("#id_article").val(id)
    $("button[name='addArticleToForm']").val(id)
    loadLibraryItemToModal(id, false)
  })
  $(document).on("click", "button[name='selectBenchmark']", function(e){
    e.preventDefault();
    let id = $(this).val();
    $("#id_benchmark").val(id)
    $("button[name='addBenchmarkToForm']").val(id)
    loadLibraryItemToModal(id, false)
  })
  $(document).on("click", "button[name='selectVideo']", function(e){
    e.preventDefault();
    let id = $(this).val();
    $("#id_video").val(id)
    $("button[name='addVideoToForm']").val(id)
    loadLibraryItemToModal(id, false)
  })


  $(document).on("click", "button[name='addArticleToForm']", function(e){
    let typeId  = $(this).val().split("_")
    let type = typeId[0]
    let id = typeId[1]
    console.log("ID", id)
    $("#id_on_pathway").val($("#pathwayId").val())
    $("#id_article").val(id)
    $("#id_content_type").val("Article")
    $("#contentSelectType").text("Article")
    $("#contentSelectTitle").text($("#articleItemTitle").text())
    $("#viewLibraryArticleResultModal").modal("hide")
    $("#selectedPathwayContent").show()
  })
  $(document).on("click", "button[name='addBenchmarkToForm']", function(e){
    let typeId  = $(this).val().split("_")
    let type = typeId[0]
    let id = typeId[1]
    $("#id_on_pathway").val($("#pathwayId").val())
    $("#id_benchmark").val(id)
    $("#id_content_type").val("Benchmark")
    $("#contentSelectType").text("Benchmark")
    $("#contentSelectTitle").text($("#benchmarkItemTitle").text())
    $("#viewLibraryBenchmarkResultModal").modal("hide")
    $("#selectedPathwayContent").show()
  })
  $(document).on("click", "button[name='addVideoToForm']", function(e){
    let typeId  = $(this).val().split("_")
    let type = typeId[0]
    let id = typeId[1]
    $("#id_on_pathway").val($("#pathwayId").val())
    $("#id_video").val(id)
    $("#id_content_type").val("Video")
    $("#contentSelectType").text("Video")
    $("#contentSelectTitle").text($("#videoItemTitle").text())
    $("#viewLibraryVideoResultModal").modal("hide")
    $("#selectedPathwayContent").show()
  })


    $("#submitCopyAim").hide()
    $("#deleteBenchmarkBookmark").hide()
    $("#deleteVideokBookmark").hide()
    $("#deleteArticleBookmark").hide()
    $("button[name='addArticleToForm']").show()

    })
