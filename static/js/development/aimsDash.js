
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
          <li class="list-group-item">
            <p>${item.question}</p>
              <ul class="nav nav flex-column">
                <li class="nav-item my-2" id="completeShow_${index}">
                </li>
                <li class="nav-item my-2" id="minShow_${index}">
                </li>
                <li class="nav-item my-2" id="noShow_${index}">
                </li>
              </ul>
          </li>`);
        if( item.tracker.minimum_show_allowed){
          if (item.count_quantity == "null"){
          $(`#minShow_${index}`).append(`
            <div class="row px-0">
              <div class="col-9">
                I showed up <small>(${item.tracker.minimum_show_description})</small>
              </div>
              <div class="col-3">
                <a type="button" class="primary"><i class="fas fa-bars"></i></a>
              </div>
            </div>
            `);
          } else {
            $(`#minShow_${index}`).append(`
              <div class="row px-0">
                <div class="col-12">
                  You've already logged ${item.count_quantity} ${item.tracker.metric_unit} today
                </div>
              </div>
              `);
          };
        } else {
          $(`#minShow_${index}`).append(`
            <div class="row px-0">
              <div class="col-12">
                Minimum show alternative not allowed.
              </div>
            </div>
            `);
          };
        if(item.tracker.metric_tracker_type =="boolean"){
          $(`#completeShow_${index}`).append(`
          <div class="row px-0">
            <div class="col-9">
              I completed this successfully
            </div>
            <div class="col-3">
              <a type="button" class="primary"><i class="fas fa-bars"></i></a>
            </div>
          </div>`);
        } else {
          $(`#completeShow_${index}`).append(`
          <div class="row px-0">
            <div class="col-9">
              <div class="input-group mb-3">
                <span class="input-group-text" id="countInput">Adding count of: </span>
                <input type="text" class="form-control" aria-label="Username" aria-describedby="countInput">
              </div>
            </div>
            <div class="col-3">
              <a type="button" class="primary"><i class="fas fa-bars"></i></a>
            </div>
          </div>`)
        };
      });
      }
    })
  };
