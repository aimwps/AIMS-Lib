
$(document).ready(function () {
  getUncompleteTrackers() ;
});
function getUncompleteTrackers() {
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
            <p>${item.question}<br><small>submission period: ${ item.period_log_start} to ${item.period_log_end}</small></p>

              <ul class="list-group">
                <li class="list-group-item border border-white" id="minShow_${index}">
                </li>
                <li class="list-group-item border border-white" id="completeShow_${index}">
                </li>
                <li class="list-group-item border border-white" id="noShow_${index}">
                </li>
              </ul>
          </li>`);
        if( item.tracker.minimum_show_allowed){
          if (item.count_quantity == null){
          $(`#minShow_${index}`).append(`
          <div class="row">
            <div class="col-3">
            </div>
            <div class="col-8">
              <p><strong>Submit, I showed up: </strong> ${item.tracker.minimum_show_description}</p>
            </div>
          </div>
            `);
          } else {
            $(`#minShow_${index}`).append(`
            <div class="row">
              <div class="col-3">
              </div>
              <div class="col-9">
                <p>You've logged ${item.count_quantity} ${item.tracker.metric_unit} already this period. The minimum show option has been disabled.</p>
              </div>
            </div>
              `);
          };
        } else {
          $(`#minShow_${index}`).append(`
          <div class="row">
            <div class="col-3">

            </div>
            <div class="col-9">
              <p>No minimum show option available for this tracker</p>
              </div>
            </div>
            `);
          };
        if(item.tracker.metric_tracker_type =="boolean"){
          $(`#completeShow_${index}`).append(`
          <div class="row">
            <div class="col-3">
            </div>
            <div class="col-9">
              <p>I completed this successfully</p>
            </div>

            </div>`)
        } else {
          $(`#completeShow_${index}`).append(`
          <div class="row">
            <div class="col-3 my-auto">
              <input type="text" class="form-control" id="inputCountValue_${index}">
            </div>
            <div class="col-9">
              <p><strong>Submit, count: </strong> Enter an amount of ${item.tracker.metric_unit} you have ${item.tracker.metric_action} this period and submit</p>
            </div>
          </div>
              `)
        };
      });
      }
    })
  };
