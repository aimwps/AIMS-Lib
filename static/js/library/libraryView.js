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
  function loadLibraryItemToModal(resultData){
    $("#viewLibraryResultModal").modal("show");

    $.ajax({
        type: "GET",
        url: "/LibraryView_ajax_get_library_result/",
        data: {result_phrase: resultData},
        datatype: "json",
        success: function(json){
          console.log(json)
        }
    })
  }
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
})
