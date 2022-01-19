$(document).ready(function(){
  getBenchmarkQaData();
});


// Retrieves a benchmarks data including question and answers
function getBenchmarkQaData(){
  $.ajax({
    method:"GET",
    url:"/ajax_get_benchmark_qa_data/",
    data: {benchmark_id: $("#benchmarkId").val()},
    datatype: "json",
    success: function(json){
      console.log(json);
      $("#questionAnswerDisplayRow").empty();
      $.each(json.questions, function(questionIdx, question){
        console.log(question);
        $("#questionAnswerDisplayRow").append(`
          <div class="col-xs-12 col-md-3 py-2 px-2">
            <div class="container py-2 border border-primary rounded">
              <ul class="list-group list-group-flush">
                <li class="list-group-item px-0"><strong>Q${question.order_position + 1}</strong> ${question.question_text}?
                  <ul id="answerList${question.id}">
                  </ul>
                </li>
              </ul>
            </div>
          </div>`);
        $.each(question.answers, function(answerIdx, answer){
          $(`#answerList${question.id}`).append(`
            <li class="list-group-item border-0 px-0">
              <span id="answerCorrect${answer.id}"></span> ${answer.answer_text}
            </li>`);
            if (answer.is_correct){
              $(`#answerCorrect${answer.id}`).append(`<i class="fas fa-check"></i>`)
            } else {
              $(`#answerCorrect${answer.id}`).append(`<i class="fas fa-times"></i>`)
            }
        })

      });

    }
  })
};

$("input[name='searchModalInput']").keyup(function(){
  if ($("input[name='searchModalInput']").length > 0){
  searchQABank();
};
});


function searchQABank(){
  $.ajax({method:"GET",
          url:"/ajax_search_qa_bank/",
          data: {benchmark_id: $("#benchmarkId").val(),
                search_phrase: $("input[name='searchModalInput']").val()},
          datatype:"json",
          success: function(json){
            $("#addQuestionSearchDisplay").empty();
            $.each(json, function(index, gqb){
                $("#addQuestionSearchDisplay").append(`
                  <li class="list-group-item">
                  ${gqb.question}
                  <ul class="list-group-flush id="gqbAnswers${gqb.id}">
                    <li class="list-group-item">
                      - ${gqb.answer}
                    </li>
                  </ul>
                  <ul class="nav justify-content-center">
                      <li class="nav-item px-2">
                        <a type="button"  data-bs-toggle="tooltip" title="edit before adding">
                          <i class="far fa-edit"></i>
                        </a>
                      </li>

                      <li class="nav-item px-2">
                          <a type="button" onclick="quickAddGQB(${gqb.id})" value="${gqb.id}" class="text-primary">
                            <i class="fas fa-plus"></i>
                          </a>
                      </li>
                  </ul>
                  </li>

                  `);
            })

          }
        });
};

// $("button[name='quickAddGQB']").click(function(e){
//   e.preventDefault();
function quickAddGQB(gqbId){
  console.log("BUM")
  console.log(gqbId)
  $.ajax({method:"POST",
          url:"/ajax_add_gqb_to_benchmark/",
          datatype:"json",
          data:{
            benchmark_id:$("#benchmarkId").val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            gqb_id:gqbId,
          },
          success: function(json){
            console.log(json);
            getBenchmarkQaData();
            $("input[name='searchModalInput']").dispatchEvent(new Event("keyup"));

          }});

};

$("#submitQAform").on('submit', function(e){
  e.preventDefault();
  $.ajax({
    type:"POST",
    url: "/ajax_create_question_answer/",
    data:{
      question:$("#questionField").val(),
      answer:$("#answerField").val(),
      benchmark_id:$("#onBenchmark").val(),
      generator_source:$("#generatedFromGqbId").val(),
      source_was_modified:$("#hasBeenModified").val(),
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
    },
    success: function(){
        // searchField.dispatchEvent(new Event("keyup"));
        getBenchmarkQaData();
    }
  });
});

// SUBMIT THE gqb AND BENCHMARK id, CREATE NEW q&a IN VIE
// respond, refresh the search, refresh the QA list

  // function getGQB(gqb_id){
  //
  //   $.ajax({
  //     method: "GET",
  //     url: "/ajax_get_gqb/",
  //     data : {gqb_id: gqb_id},
  //     datatype : json,
  //     success : function(json){
  //       console.log(json);
  //     }
  //   })};


$("button[name='quickAddGQB']").on('click', function(){
  console.log("BUM")
  let gqbId = $(this).val();
  console.log(gqbId)
  $.ajax({method:"POST",
          url:"/ajax_add_gqb_to_benchmark/",
          datatype:"json",
          data:{
            benchmark_id:$("#benchmarkId").val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            gqb_id:gqbId,
          },
          success: function(json){
            console.log(json);
            getBenchmarkQaData();
            $("input[name='searchModalInput']").dispatchEvent(new Event("keyup"));

          }});

});
