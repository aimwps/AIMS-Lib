
// Retrieves a benchmarks data including question and answers
$(document).ready(function(){
  function addAnswer(questionId){
  $("#addAnswerModal").toggle();
  }
  function getBenchmarkQaData(){
    $("#questionField").val("");
    $("#answerField").val("");
    $("#generatedFromGqbId").val("");
    $("#hasBeenModified").val("");
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
                  <li class="list-group-item px-0">
                      <strong class="text-primary">Q${question.order_position + 1}</strong> ${question.question_text}?
                      <ul id="answerList${question.id}" class="list-group list-group-flush">
                      </ul>
                  </li>
                </ul>
                <div class="text-center">
                  <ul class="nav justify-content-center">
                      <li class="nav-item">
                        <button class="btn btn-link" type="button" name="addAnswer" value="${question.id}" data-bs-toggle="tooltip" title="add an answer">
                          <i class="fas fa-plus text-primary"></i>
                        </button>
                      </li>

                      <li class="nav-item">
                        <button class="btn btn-link" data-bs-toggle="tooltip" title="edit question settings">
                          <i class="far fa-edit"></i>
                        </button>
                      </li>

                      <li class="nav-item">
                        <button class="btn btn-link" data-bs-toggle="tooltip" title="test question">
                          <i class="fas fa-vial"></i>
                        </button>
                      </li>
                  </ul>
                </div>
              </div>
            </div>`);
          $.each(question.answers, function(answerIdx, answer){
            $(`#answerList${question.id}`).append(`
              <li class="list-group-item border-0 px-0">
                <button name="answerSelect" class="btn btn-al w-100 py-2 text-start">
                <span id="answerCorrect${answer.id}"></span> ${answer.answer_text}
                </button>
              </li>`);
              if (answer.is_correct){
                $(`#answerCorrect${answer.id}`).append(`<i class="fas fa-check text-primary"></i>`)
              } else {
                $(`#answerCorrect${answer.id}`).append(`<i class="fas fa-times text-primary"></i>`)
              }
          })

        });

      }
    })
  };
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

  getBenchmarkQaData();


  $(document).on('click', "button[name='addAnswer']", function(event){
    let QuestionId = $(this).val();
    $('#id_on_question').val(QuestionId);
    $('#addAnswerModal').modal("toggle");

  });

  $(document).on('click', "button[id='submitNewAnswer']", function(event){
    $.ajax({
        method:"POST",
        url: "/ajax_add_answer/",
        data: {
              on_question : $("#id_on_question").val(),
              csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
              source_was_modified: $("#id_source_was_modified").val(),
              generator_source:$("#id_generator_source").val(),
              answer_text: $("#id_answer_text").val(),
              is_correct: $("#id_is_correct").val(),
              is_default: $("#id_is_default").val(),
            },
        datatype: "json",
        success: function(json){
          console.log(json);
          getBenchmarkQaData();
          $('#addAnswerModal').modal("toggle");
          $("#id_on_question").val("")
          $('input[name=csrfmiddlewaretoken]').val("")
          $("#id_source_was_modified").val("")
          $("#id_generator_source").val("")
          $("#id_answer_text").val("")
          $("#id_is_correct").val("")
          $("#id_is_default").val("")

        }
    })
  });


  $("input[name='searchModalInput']").keyup(function(){
    if ($("input[name='searchModalInput']").val().length > 0){
    searchQABank();
  } else {
    $("#addQuestionSearchDisplay").empty();
  };
  });

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

})
