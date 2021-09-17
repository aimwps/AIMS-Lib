
$(document).ready(function () {
  getUnverifiedGqb() ;
});
function getUnverifiedGqb() {
  $('#unverifiedGQB').empty();
  $.ajax({
    type: "GET",
    url: "/get-gqb-to-verify/",
    success: function(gqb) {
      $.each(gqb, function(i, item){
          $('#unverifiedGQB').append(`
          <li class="list-group-item"><strong>Q: </strong>${item.question}
            <div class="container">
              <strong>A:</strong> ${item.answer}
              <ul class="list-group list-group-horizontal">
                <li class="list-group-item border-0"><a href='#'>View source</a></li>
                <li class="list-group-item border-0">Rate the quality:</li>
                <li class="list-group-item border-0"><a type="button" class="text-primary" onClick="submitGqbStatus(${item.id}, 'perfect')">Perfect</a></li>
                <li class="list-group-item border-0"><a type="button"class="text-primary"  onClick="submitGqbStatus(${item.id}, 'iffy')">Iffy</a></li>
                <li class="list-group-item border-0"><a type="button"class="text-primary"  onClick="submitGqbStatus(${item.id}, 'incorrect')">Incorrect</a></li>
              </ul>
            </div>
            </li>`)
      });
      }
    })
  } ;


function submitGqbStatus(gqb_id, gqb_status) {
  $.ajax({
    type:"POST",
    url: "/submit-gqb-verification/",
    data:{
          submit_id: gqb_id,
          submit_status: gqb_status,
          csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    },
    success: function(){
        getUnverifiedGqb();
    }
  })
};
