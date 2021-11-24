/*jslint browser: true*/
/*global $, jQuery, alert*/

$(document).ready(function () {
  getUncompleteTrackers() ;
});
function getUncompleteTrackers() {
  $("#displayToday").empty();
  $("#displayWeek").empty();
  $("#displayMonth").empty();
  $("#displayYear").empty();
  $.ajax({
    type: "GET",
    url: "/get_quickfire_trackers/",
    data: {
      user_id:$("input[name=user_id]").val(),
    },
    datatype: 'json',
    success: function(trackerLogPeriod) {
      $.each(trackerLogPeriod, function(index, item){
        console.log(item);
        var selectDisplay = `#${item.display_section}`;
        console.log(selectDisplay)
        $(selectDisplay).append(`
          <li class="list-group-item border border-primary my-2">
            <p>${item.question}<br>
            <small>Period start: ${ item.pretty_start}</small><br>
            <small>Period end:${item.pretty_end}<br>

              <ul class="list-group">
                <li class="list-group-item border border-white" id="completeShow_${index}">
                </li>
                <li class="list-group-item border border-white" id="minShow_${index}">
                </li>
                <li class="list-group-item border border-white" id="noShow_${index}">
                <div class="row">
                  <div class="col-10  text-end">
                  <p><strong>Submit, incomplete: </strong><small>Try another day (period progress is over written)</small></p>
                  </div>
                  <div class="col-2 my-auto">
                  <a type="button" class="link link-primary" onClick="submitUncomplete(${item.tracker.id})"><p class="lead"><i class="fas fa-recycle"></i></p></a>
                  </div>
                </div>
                </li>
              </ul>
          </li>`);
        if( item.tracker.minimum_show_allowed){
          if (item.count_quantity == null){
          $(`#minShow_${index}`).append(`
          <div class="row">
            <div class="col-10 text-end">
              <p><strong>Submit show up: </strong><small>${item.tracker.minimum_show_description}</small></p>
            </div>
            <div class="col-2">
              <a type="button" class="link link-primary" onClick="submitShowup(${item.tracker.id})"><p class="lead"><i class="fas fa-compress"></i></p></a>
            </div>
          </div>
            `);
          } else {
            $(`#minShow_${index}`).append(`
            <div class="row">
              <div class="col-10 text-end">
                <p><strong>Show up, unavailable: </strong><small>You've logged ${item.count_total} ${item.tracker.metric_unit} this period</small></p>
              </div>
              <div class="col-2">
              <p class="lead"><i class="fas fa-compress"></i></p>
              </div>
            </div>
              `);
          };
        } else {
          $(`#minShow_${index}`).append(`
          <div class="row">
            <div class="col-10 text-end">
              <p><strong>Show up, unavailable : </strong><small>No minimum show alternative</small></p>
              </div>
              <div class="col-2">
                <p class="lead"><i class="fas fa-compress"></i></p>
              </div>
            </div>
            `);
          };
        if(item.tracker.metric_tracker_type =="boolean"){
          $(`#completeShow_${index}`).append(`
          <div class="row">
            <div class="col-10 text-end">
              <p><strong>Submit success: </strong><small>You completed your step successully</small></p>
            </div>
            <div class="col-2">
              <a type="button" class="link link-primary"  onClick="submitBooleanComplete(${item.tracker.id})"><p class="lead"><i class="fas fa-rocket"></i></p></a>
            </div>
            </div>`)
        } else {
          $(`#completeShow_${index}`).append(`
          <div class="row">
            <div class="col-10 text-end">
              <div class="row form-group">
                <label class="col-9 col-form-label" for="inputCountValue_${index}"><strong>Submit count: </strong><small>${item.tracker.metric_unit}</small></label>
                <div class="col-3 my-auto">
                  <input type="text" class="form-control px-1" id="inputCountValue_${index}">
                </div>
              </div>
            </div>
            <div class="col-2 my-auto">
                <a type="button" class="link link-primary"  onClick="submitCount(${item.tracker.id}, ${index})"><p class="lead"><i class="fas fa-rocket"></i></p></a>
            </div>
          </div>
              `)
        };
      });
      }
    })
  };

function submitBooleanComplete(tracker_id){
  console.log(tracker_id);
  $.ajax({
    type: "POST",
    url: "/submit_tracker/",
    data: {tracker_id: tracker_id,
          csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
          submit_type: "boolean_success",
          submit_user: $("input[name=user_id]").val(),
    },
    success: function(){
      getUncompleteTrackers();
    }
  })
};

function submitShowup(tracker_id){
  console.log(tracker_id);
  $.ajax({
    type: "POST",
    url: "/submit_tracker/",
    data: {tracker_id: tracker_id,
          csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
          submit_type: "min_showup",
          submit_user: $("input[name=user_id]").val(),
    },
    success: function(){
      getUncompleteTrackers();
    }

  })

};
function submitCountShowup(tracker_id){
  console.log(tracker_id);
  $.ajax({
    type: "POST",
    url: "/submit_tracker/",
    data: {tracker_id: tracker_id,
          csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
          submit_type: "count_showup",
          submit_user: $("input[name=user_id]").val(),
    },
    success: function(){
      getUncompleteTrackers();
    }

  })

};
function submitUncomplete(tracker_id){
  console.log(tracker_id);
  $.ajax({
    type: "POST",
    url: "/submit_tracker/",
    data: {tracker_id: tracker_id,
          csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
          submit_type: "fail_or_no_submit",
          submit_user: $("input[name=user_id]").val(),
    },
    success: function(){
      getUncompleteTrackers();
    }

  })

};
function submitCount(tracker_id, index){
  console.log(tracker_id);
  $.ajax({
    type: "POST",
    url: "/submit_tracker/",
    data: {tracker_id: tracker_id,
          csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
          submit_type: "count_value",
          submit_user: $("input[name=user_id]").val(),
          count_value: $(`#inputCountValue_${index}`).val()
    },
    success: function(){
      getUncompleteTrackers();
    }

  })

};
function getCalmapData(tracker_id){
  $.ajax({
        type : "GET",
        url : "/get_calmap_data/",
        data : {tracker_id : tracker_id,},
        datatype: 'json',
        success : function(trackerData){
          // console.log("trackerData", trackerData);
          const dataInfo = JSON.parse(trackerData);
          // console.log("dataInfo", dataInfo);
          var sd = new Date(dataInfo.calmap_settings.sd*1000);
          var ed = new Date(dataInfo.calmap_settings.ed*1000);
          ed.setMonth( ed.getMonth() + 2 );
          var now = new Date();
          now.setMonth(now.getMonth()-1);
          var cal = new CalHeatMap();
          $("#CalmapModalBody").empty();
          cal.init({itemSelector:"#CalmapModalBody",
                    domain:"month",
                    subdomain:"day",
                    range: 3,
                    dataType:"json",
                    data: dataInfo.calmap_data,
                    previousSelector: "#CalmapModalBody-prev",
                  	nextSelector: "#CalmapModalBody-next",
                    itemNamespace: "cal",
                    cellPadding: 5,
                  	domainGutter: 20,
                    domainDynamicDimension: false,
                    cellSize: 30,
                    cellRadius: 0,
                    start: new Date(now),
                    minDate: sd,
                    maxDate: ed,
                    subDomainTextFormat: "%d",
                    weekStartOnMonday: true,
                    // label: {
                    //   height:100,
                    // },
                    legendCellSize: 20,
                    legend:[1,500, 575, 650, 725,800, 875, 950,1000],
                    displayLegend: false,
                    // legendColors: {//min:"white",
                    //               //max:"#c6471b",
                    //               empty: "grey",
                    //               base: "grey",
                    //
                    //             },
                    tooltip: false,
                    subDomainTitleFormat: {empty: "{date}", filled: "{date}" },
                    onClick: function(date, nb) {
                      console.log(dataInfo.count_data);
                      var userTimezoneOffset = date.getTimezoneOffset() * 60000;
                      var adjDate = new Date(date.getTime() - userTimezoneOffset);
                      var dateID = Math.floor(adjDate.getTime()/1000);
                      let count =  dataInfo.count_data[dateID][0];
                      var startDate = dataInfo.count_data[dateID][1];
                      var endDate = dataInfo.count_data[dateID][2];
                      $(".clearme").empty();
                      $("#onClickDisplayPS").html(startDate);
                      $("#onClickDisplayPE").html(endDate);
                      $("#onClickDisplaySM").html(count);

                    }


                  });
      }})
};

function search(source, name) {
    var results;

    name = name.toUpperCase();
    results = $.map(source, function(entry) {
        var match = entry.name.toUpperCase().indexOf(name) !== -1;
        return match ? entry : null;
    });
    return results;
}

// function loadCalmapToModal(trackerData){
//
//
//
// };
