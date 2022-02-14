$(document).ready(function(){
  function ajaxSearchLibrary(searchPhrase){
    $.ajax({
      type:"GET",
      url: "/LibraryView_ajax_search_library/",
      datatype:"json",
      data: {"search_phrase": searchPhrase},
      success: function(json){
        console.log(json)
        // Display all result
        $.each(json, function(field_idx, result_field){
          $.each(result_field, function(result_idx, result){

            if(result.library_type === "StepTracker"){
              $("#AllResultsList").append(`
                <li class="list-group-item">
                <button class="btn btn-link text-start  px-0" name="viewLibraryItem" value="${result.library_type}_${result.id}">
                  ${result.library_type}: ${result.library_title}
                 </button>
                <br>
                <small> ${result.library_description}..</small>
                </li>
                `);
              $("#StepTrackerResultsList").append(`
                <li class="list-group-item">
                <button class="btn btn-link text-start  px-0" name="viewLibraryItem" value="${result.library_type}_${result.id}">
                  ${result.library_type}: ${result.library_title}
                 </button>
                <br>
                <small> ${result.library_description}..</small>
                </li>
                `)

            } else if(result.library_type === "Behaviour"){
              $("#AllResultsList").append(`
                <li class="list-group-item">
                <button class="btn btn-link text-start  px-0" name="viewLibraryItem" value="${result.library_type}_${result.id}">
                  ${result.library_type}: ${result.library_title}
                 </button>
                <br>
                <small> ${result.library_description}..</small>
                </li>
                `);
              $("#BehaviourResultsList").append(`
                <li class="list-group-item">
                <button class="btn btn-link text-start  px-0" name="viewLibraryItem" value="${result.library_type}_${result.id}">
                  ${result.library_type}: ${result.library_title}
                 </button>
                <br>
                <small> ${result.library_description}..</small>
                </li>
                `);
            } else {
            $("#AllResultsList").append(`
              <li class="list-group-item">
              <button class="btn btn-link text-start  px-0" name="viewLibraryItem" value="${result.library_type}_${result.id}">
                ${result.library_type}: ${result.library_title}
               </button>
              <br>
              <small> ${result.library_description}..</small>
              </li>
              `);
            let contentListId = `#${result.library_type}ResultsList`
            $(contentListId).append(`
              <li class="list-group-item">
              <button class="btn btn-link text-start  px-0" name="viewLibraryItem" value="${result.library_type}_${result.id}">
                ${result.library_type}: ${result.library_title}
               </button>
              <br>
              <small> ${result.library_description}..</small>
              </li>
              `)
          }
      })
    })
  }})
  };
  function loadAimItemToModal(aimData){
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
  function loadBehaviourItemToModal(behaviourData){
    $("#behaviourTrackers").empty()
    $("#viewLibraryBehaviourResultModal").modal("show")
    $("#behaviourTitle").text(behaviourData.title)
    $("#submitBookmarkBehaviour").val(behaviourData.id)
    $.each(behaviourData.trackers, function(idx, tracker){
      $("#behaviourTrackers").append(`
        <li class="list-group-item border-0">

          <a class="btn-link nounderline" data-bs-toggle="collapse" href="#trackerCollapse_${tracker.id}" role="button" aria-expanded="false" aria-controls="trackerCollapse_${tracker.id}">
            ${tracker.get_tsentence}
          </a>

            <div class="collapse" id="trackerCollapse_${tracker.id}">
              <div class="card card-body border-0 px-0">
                <ul class="list-group-flush px-0" id="behaviours_${tracker.id}_tracker_list">
                  <li class="list-group-item border-0">
                  <small><strong>Type: </strong>${tracker.get_type_sentence}</small>
                    </li>
                  <li class="list-group-item border-0">
                  <small><strong>Frequency: </strong>${tracker.get_frequency_sentence}</small>
                    </li>
                  <li class="list-group-item border-0">
                  <small><strong>Log window: </strong>A ${tracker.record_log_length}</small>
                    </li>
                    </li>
                </ul>
              </div>
            </div>

        </li>
        `);

      })

    };
  function loadStepTrackerItemToModal(tracker){
    console.log(tracker)
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
  function loadOrganisationItemToModal(organisationData){
      $("#viewLibraryOrganisationResultModal").modal("show")
      $("#submitBookmarkOrganisation").val(organisationData.id)
      $("#organsationDetails").empty()
      $("#organsationDetails").append(`
        <li class="list-group-item">
        <small><strong>Title: </strong>${organisationData.title}</small>
        </li>
        <li class="list-group-item">
        <small><strong>Description: </strong>${organisationData.description}</small>
        </li>
        `)
  }
  function loadVideoItemToModal(videoData){
      $("#viewLibraryVideoResultModal").modal("show")
      $("#submitBookmarkVideo").val(videoData.id)
      $("#videoDetails").empty()
      $("#videoDetails").append(`
        <li class="list-group-item">
        <small><strong>Title: </strong>${videoData.title}</small>
        </li>
        `)
  }

  function loadArticleItemToModal(articleData){
      $("#viewLibraryArticleResultModal").modal("show")
      $("#submitBookmarkArticle").val(articleData.id)
      $("#articleDetails").empty()
      $("#articleDetails").append(`
        <li class="list-group-item">
        <small><strong>Title: </strong>${articleData.title}</small>
        </li>
        <li class="list-group-item">
        <small><strong>Description: </strong>${articleData.description}</small>
        </li>
        `)
  }

  function loadBenchmarkItemToModal(benchmarkData){
      $("#viewLibraryBenchmarkResultModal").modal("show")
      $("#submitBookmarkBenchmark").val(benchmarkData.id)
      $("#benchmarkDetails").empty()
      $("#benchmarkDetails").append(`
        <li class="list-group-item">
        <small><strong>Title: </strong>${benchmarkData.title}</small>
        </li>
        <li class="list-group-item">
        <small><strong>Description: </strong>${benchmarkData.description}</small>
        </li>
        `)
  }

  function loadPathwayItemToModal(pathwayData){
      $("#viewLibraryPathwayResultModal").modal("show")
      $("#submitBookmarkPathway").val(pathwayData.id)

      $("#pathwayDetails").append(`
        <li class="list-group-item">
        <small><strong>Title: </strong>${pathwayData.title}</small>
        </li>
        <li class="list-group-item">
        <small><strong>Description: </strong>${pathwayData.description}</small>
        </li>
        `)
  }
  function loadLibraryItemToModal(resultData){
        $.ajax({
        type: "GET",
        url: "/LibraryView_ajax_get_library_result/",
        data: {result_phrase: resultData},
        datatype: "json",
        success: function(json){
          console.log(json)
          if (json.library_type ==="Aim"){
            loadAimItemToModal(json);
          } else if (json.library_type === "Behaviour"){
            loadBehaviourItemToModal(json);
          } else if (json.library_type === "StepTracker"){
            loadStepTrackerItemToModal(json);
          } else if (json.library_type === "Organisation"){
            loadOrganisationItemToModal(json);
          } else if (json.library_type === "Video"){
            loadVideoItemToModal(json);
          } else if (json.library_type === "Article"){
            loadArticleItemToModal(json);
          } else if (json.library_type === "Benchmark"){
            loadBenchmarkItemToModal(json);
          } else if (json.library_type === "Pathway"){
            loadPathwayItemToModal(json);
         } else {
            console.log("we haven't uinderstood the contentType")
          };
    }})
  }
  function submitUseLibraryContent(contentId, contentType, submitType){
    $.ajax({type:"POST",
            url:"/LibraryView_ajax_use_content/",
            datatype:"json",
            data:{content_id: contentId,
                  content_type: contentType,
                  submit_type: submitType,
                  csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),},
            success: function(json){
              console.log(json);
              getUserBookmarks()
              $("#viewLibraryAimResultModal").modal("hide")
              $("#viewLibraryBehaviourResultModal").modal("hide")
              $("#viewLibraryStepTrackerResultModal").modal("hide")
              $("#viewLibraryVideoResultModal").modal("hide")
              $("#viewLibraryArticleResultModal").modal("hide")
              $("#viewLibraryBenchmarkResultModal").modal("hide")
              $("#viewLibraryOrganisationResultModal").modal("hide")
              $("#viewLibraryPathwayResultModal").modal("hide")
            }})
  }
  function getUserBookmarks(){
    $("ul.bookmarkresultlist").empty();
    $.ajax({
              type:"GET",
              url:"/LibraryView_ajax_get_user_bookmarks/",
              datatype: "json",
              success: function(json){
                console.log(json)
                if (json.length > 0){
                  $.each(json, function(idx, bookmark){
                    if (bookmark.content_type === "Article"){
                      $("#ArticleUserBookmarks").append(`
                        <li class="list-group-item">
                        ${bookmark.article.title}
                        </li>`)
                      $("#AllUserBookmarks").append(`
                        <li class="list-group-item">
                        ${bookmark.article.title}
                        </li>`)
                    } else if (bookmark.content_type ==="VideoLecture"){
                      $("#VideoUserBookmarks").append(`
                        <li class="list-group-item">
                        ${bookmark.video.title}
                        </li>`)
                      $("#AllUserBookmarks").append(`
                        <li class="list-group-item">
                        ${bookmark.video.title}
                        </li>`)
                    } else if (bookmark.content_type ==="Benchmark"){
                      $("#BenchmarkUserBookmarks").append(`
                        <li class="list-group-item">
                        ${bookmark.benchmark.title}
                        </li>`)
                      $("#AllUserBookmarks").append(`
                        <li class="list-group-item">
                        ${bookmark.benchmark.title}
                        </li>`)
                    } else if (bookmark.content_type ==="Pathway") {
                      $("#PathwayUserBookmarks").append(`
                        <li class="list-group-item">
                        ${bookmark.pathway.title}
                        </li>`)
                      $("#AllUserBookmarks").append(`
                        <li class="list-group-item">
                        ${bookmark.pathway.title}
                        </li>`)
                    } else if (bookmark.content_type ==="Organisation") {
                      $("#OrganisationUserBookmarks").append(`
                        <li class="list-group-item">
                        ${bookmark.organisation.title}
                        </li>`)
                      $("#AllUserBookmarks").append(`
                        <li class="list-group-item">
                        ${bookmark.organisation.title}
                        </li>`)
                    } else if (bookmark.content_type ==="Aim") {
                      $("#AimUserBookmarks").append(`
                        <li class="list-group-item">
                        ${bookmark.aim.title}
                        </li>`)
                      $("#AllUserBookmarks").append(`
                        <li class="list-group-item">
                        ${bookmark.aim.title}
                        </li>`)
                    }  else if (bookmark.content_type ==="Behaviour") {
                      $("#BehaviourUserBookmarks").append(`
                        <li class="list-group-item">
                        ${bookmark.behaviour.title}
                        </li>`)
                      $("#AllUserBookmarks").append(`
                        <li class="list-group-item">
                        ${bookmark.behaviour.title}
                        </li>`)
                    }  else if (bookmark.content_type ==="StepTracker") {
                      $("#StepTrackerUserBookmarks").append(`
                        <li class="list-group-item">
                        ${bookmark.steptracker.get_tsentence}
                        </li>`)
                      $("#AllUserBookmarks").append(`
                        <li class="list-group-item">
                        ${bookmark.steptracker.get_tsentence}
                        </li>`)
                    }

                    else {
                      console.log("errors with content type")
                    }
                  })
                } else{
                  console.log("no records found")
                }

              }
    })
  }


  $(document).on("keyup", "#searchInput", function(){
    let searchPhrase = $(this).val();
    if (searchPhrase.length > 0 & searchPhrase != " "){
        ajaxSearchLibrary(searchPhrase);
      } else {
        $("#AllResultsList").empty();
        $("ul.resultlist").empty();
      }

  });

    $(document).on("click", "#resetLibrarySearch", function(e){
      e.preventDefault();
      $("#searchInput").val("")
      $("#AllResultsList").empty();
      $("ul.resultlist").empty();

    })
  $(document).on("click", "[name='viewLibraryItem']", function(){
    let itemData = $(this).val();
    loadLibraryItemToModal(itemData);
  })

  $(document).on("click", "#submitCopyAim", function(e){
    e.preventDefault();
    let aimId = $(this).val();
    submitUseLibraryContent(aimId,"Aim","copy")
  })
  $(document).on("click", "#submitBookmarkAim", function(e){
    e.preventDefault();
    let aimId = $(this).val();
    submitUseLibraryContent(aimId,"Aim","bookmark")
  })


  $(document).on("click", "#submitBookmarkBehaviour", function(e){
    e.preventDefault();
    let id = $(this).val()
    submitUseLibraryContent(id,"Behaviour","bookmark")
  })

  $(document).on("click", "#submitBookmarkStepTracker", function(e){
    e.preventDefault();
    let id = $(this).val()
    submitUseLibraryContent(id,"StepTracker","bookmark")
  })

  $(document).on("click", "#submitBookmarkOrganisation", function(e){
    e.preventDefault();
    let id = $(this).val()
    submitUseLibraryContent(id,"Organisation","bookmark")
  })
  $(document).on("click", "#submitBookmarkPathway", function(e){
    e.preventDefault();
    let id = $(this).val()
    submitUseLibraryContent(id,"Pathway","bookmark")
  })
  $(document).on("click", "#submitBookmarkArticle", function(e){
    e.preventDefault();
    let id = $(this).val()
    submitUseLibraryContent(id,"Article", "bookmark")
  })
  $(document).on("click", "#submitBookmarkVideo", function(e){
    e.preventDefault();
    let id = $(this).val()
    submitUseLibraryContent(id,"VideoLecture","bookmark")
  })
  $(document).on("click", "#submitBookmarkBenchmark", function(e){
    e.preventDefault();
    let id = $(this).val()
    submitUseLibraryContent(id,"Benchmark","bookmark")
  })
  getUserBookmarks()
})
