$(document).ready(function(){
  function ajaxSearchLibrary(searchPhrase){
    $.ajax({
      type:"GET",
      url: "/LibraryView_ajax_search_library/",
      datatype:"json",
      data: {"search_phrase": searchPhrase},
      success: function(json){
        console.log(json)
        // Display all results
        $("#allResultsList").empty();
        $.each(json, function(field_idx, result_field){
          $.each(result_field, function(result_idx, result){
            let descriptionOrMotivation = (result.library_description)? result.library_description: result.motivation;
            $("#allResultsList").append(`
              <li class="list-group-item">
              <button class="btn btn-link text-start  px-0" name="viewLibraryItem" value="${result.library_type}_${result.id}">
                ${result.library_type}: ${result.title}
               </button>
              <br>
              <small> ${descriptionOrMotivation}..</small>
              </li>
              `)
          });
        });

      // Display Aims Results
      $("#aimsResultsList").empty();
      $.each(json.aims, function(result_idx, result){
        $("#aimsResultsList").append(`
          <li class="list-group-item">
          <button class="btn btn-link text-start  px-0" name="viewLibraryItem" value="${result.library_type}_${result.id}">
            ${result.library_type}: ${result.title}
           </button>
          <br>
          <small> ${result.motivation}..</small>
          </li>
          `)
      })

      // Display Pathway Results
      $("#pathwaysResultsList").empty();
      $.each(json.pathways, function(result_idx, result){
        $("#pathwaysResultsList").append(`
          <li class="list-group-item">
          <button class="btn btn-link text-start  px-0" name="viewLibraryItem" value="${result.library_type}_${result.id}">
            ${result.library_type}: ${result.title}
           </button>
          <br>
          <small> ${result.library_description}..</small>
          </li>
          `)
      })
      // Display article Results
      $("#articlesResultsList").empty();
      $.each(json.articles, function(result_idx, result){
        $("#articlesResultsList").append(`
          <li class="list-group-item">
          <button class="btn btn-link text-start  px-0" name="viewLibraryItem" value="${result.library_type}_${result.id}">
            ${result.library_type}: ${result.title}
           </button>
          <br>
          <small> ${result.library_description}..</small>
          </li>
          `)
      })

      // Display Video Results
      $("#videosResultsList").empty();
      $.each(json.videos, function(result_idx, result){
        $("#videosResultsList").append(`
          <li class="list-group-item">
          <button class="btn btn-link text-start  px-0" name="viewLibraryItem" value="${result.library_type}_${result.id}">
            ${result.library_type}: ${result.title}
           </button>
          <br>
          <small> ${result.library_description}..</small>
          </li>
          `)
      })
      // Display benchjmark Results
      $("#benchmarksResultsList").empty();
      $.each(json.benchmarks, function(result_idx, result){
        $("#benchmarksResultsList").append(`
          <li class="list-group-item">
          <button class="btn btn-link text-start  px-0" name="viewLibraryItem" value="${result.library_type}_${result.id}">
            ${result.library_type}: ${result.title}
           </button>
          <br>
          <small> ${result.library_description}..</small>
          </li>
          `)
      })

      // Display organisation Results
      $("#organisationsResultsList").empty();
      $.each(json.organisations, function(result_idx, result){
        $("#organisationsResultsList").append(`
          <li class="list-group-item">
          <button class="btn btn-link text-start  px-0" name="viewLibraryItem" value="${result.library_type}_${result.id}">
            ${result.library_type}: ${result.title}
           </button>
          <br>
          <small> ${result.library_description}..</small>
          </li>
          `)
      })
      }
    })
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
  function loadLibraryItemToModal(resultData){
        $.ajax({
        type: "GET",
        url: "/LibraryView_ajax_get_library_result/",
        data: {result_phrase: resultData},
        datatype: "json",
        success: function(json){
          console.log(json)
          if (json.library_type ==="Aim"){
            loadAimItemToModal(json)
          }
        }
    })
  }
  function submitCopyAim(aimId){
    $.ajax({type:"POST",
            url:"/LibraryView_ajax_use_content/",
            datatype:"json",
            data:{submitCopyAim: aimId,
                  csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),},
            success: function(json){
              console.log(json);
            }})
  }
  function submitBookmarkAim(aimId){
    $.ajax({type:"POST",
            url:"/LibraryView_ajax_use_content/",
            datatype:"json",
            data:{submitBookmarkAim: aimId,
                  csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),},
            success: function(json){
              console.log(json);
            }})
  };

  $(document).on("keyup", "#searchInput", function(){
    let searchPhrase = $(this).val();
    if (searchPhrase.length > 0){
        ajaxSearchLibrary(searchPhrase);
        }
  });

  $(document).on("click", "[name='viewLibraryItem']", function(){
    let itemData = $(this).val();
    loadLibraryItemToModal(itemData);
  })

  $(document).on("click", "#submitCopyAim", function(e){
    e.preventDefault();
    let aimId = $(this).val();
    submitCopyAim(aimId);
  })
  $(document).on("click", "#submitBookmarkAim", function(e){
    e.preventDefault();
    let aimId = $(this).val();
    submitBookmarkAim(aimId);
  })
})
