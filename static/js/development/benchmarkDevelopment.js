
// Retrieves a benchmarks data including question and answers
$(document).ready(function(){
  function setCrudModalUpdate(){
    console.log("called update");
    $("#crudModalPostType").val("update");
    $("#crudModalDeleteCollapseBtn").show();
    $("#crudModalDeleteCollapse").collapse("hide");
  };
  function setCrudModalCreate(){
    console.log("called create");
    $("#crudModalPostType").val("create");
    $("#crudModalDeleteCollapseBtn").hide();
    $("#crudModalDeleteCollapse").collapse("hide");
    $("#AnswerModalLabel").empty().append("Adding new answer");
    $("#answerBtnText").empty().append("Add new answer");
    $("#answerId").val("")
    $('#AnswerModal').modal("toggle");
  };
  function crudModalPost(){
    $.ajax({
        method:"POST",
        url: "/ajax_submit_answer_crud/",
        data: {
              crud_type: $("#crudModalPostType").val(),
              answer_id: $("#answerId").val(),
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
          $('#createAnswerModal').modal("toggle");
          $("#id_on_question").val("")
          $("#id_source_was_modified").val("")
          $("#id_generator_source").val("")
          $("#id_answer_text").val("")
          $("#id_is_correct").val("")
          $("#id_is_default").val("")
          $("#crudModalDeleteCheckInput").val("");
          $('#AnswerModal').modal("toggle");

        }
    });
  }
  // function createAnswer(questionId){
  // $("#createAnswerModal").toggle();
  // }
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
              <div class="container py-2 border border-primary rounded px-0">
                <ul class="list-group list-group-flush px-2">
                  <li class="list-group-item px-0 py-0">
                      <strong class="text-primary">Q${question.order_position + 1}</strong> ${question.question_text}?
                      <ul id="answerList${question.id}" class="list-group list-group-flush">
                      </ul>
                  </li>
                </ul>
                <div class="text-center">
                  <ul class="nav justify-content-center">
                      <li class="nav-item">
                        <button class="btn btn-link" type="button" name="createAnswer" value="${question.id}" data-bs-toggle="tooltip" title="add an answer">
                          <i class="fas fa-plus text-primary"></i>
                        </button>
                      </li>

                      <li class="nav-item">
                        <button class="btn btn-link" data-bs-toggle="tooltip" name="editQuestion" value="${question.id}" title="edit question settings">
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
              <li class="list-group-item border-0 px-0 py-1">
                <button name="answerEditSelect" value="${answer.id}" class="btn btn-al w-100 text-start">
                <span id="answerCorrect${answer.id}"></span> ${answer.answer_text}
                </button>
              </li>`);
              if (answer.is_correct){
                $(`#answerCorrect${answer.id}`).append(`<i class="fas fa-check text-primary"></i>`)
              } else {
                $(`#answerCorrect${answer.id}`).append(`<i class="fas fa-times text-black"></i>`)
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
                            <button type="button" name="quickAddGQB" value="${gqb.id}" class="btn btn-link">
                              <i class="fas fa-plus"></i>
                            </button>
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
              // $("input[name='searchModalInput']").dispatchEvent(new Event("keyup"));

            }});

  };
  function clearAllFormInputs(){
    $("[name='answer_text']").val("");
    $("[name='question_text']").val("");
  }

  getBenchmarkQaData();

  $(document).on('click', "[name='quickAddGQB']", function(event){
      let gqbId = $(this).val();
      console.log(gqbId);
      quickAddGQB(gqbId);
  })

  $(document).on('click', "#crudModalDeleteCheckSubmit", function(event){
  event.preventDefault();
    $("#crudModalPostType").val("delete");
    crudModalPost()

});
  $(document).on('click', "button[name='createAnswer']", function(event){
    let questionId = $(this).val();
    console.log(`question id = ${questionId}`)
    $("#id_on_question").val(questionId)
    $("#id_source_was_modified").val("")
    $("#id_generator_source").val("")
    $("#id_answer_text").val("")
    $("#id_is_correct").val("True")
    $("#id_is_default").val("False")
    setCrudModalCreate();

  });
  $(document).on('click', "button[name='editQuestion']", function(event){
    clearAllFormInputs()
    let questionId = $(this).val();
    $('#editQuestionModal').modal("toggle");
    $.ajax({method:"GET",
            url: "/ajax_get_question_data/",
            data:{question_id:questionId,},
            datatype: "json",
            success: function(json){
              console.log(json);
              $("#editQuestionId").val(json.id)
              $("#id_question_text").val(json.question_text)
              $("#id_answer_type").val(json.answer_type)
              $("#id_order_position").val(json.order_position +1)
            }
          })
  });
  $(document).on('click', "button[name='submitEditQuestion']", function(event){
    event.preventDefault();
    $.ajax({method:"POST",
            url: "/ajax_submit_question_update/",
            data:{  question_id: $("#editQuestionId").val(),
                    question_text: $("#id_question_text").val(),
                    answer_type:$("#id_answer_type").val() ,
                    order_position :$("#id_order_position").val()-1,
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),},
            datatype: "json",
            success: function(json){
              console.log(json);
              $('#editQuestionModal').modal("toggle");
              getBenchmarkQaData();
            }
          })
  });
  $(document).on('click', "button[name='answerEditSelect']", function(event){
    event.preventDefault();
    setCrudModalUpdate()
    let answerId = $(this).val();
    console.log(answerId)
    $.ajax({method:"GET",
            url: "/ajax_get_answer_data/",
            data:{answer_id: answerId,},
            datatype: "json",
            success: function(json){
              console.log(json);
              $("#AnswerModal").modal("toggle");
              $("#AnswerModalLabel").empty().append("Editing an answer");
              $("#answerBtnText").empty().append("Update answer")
              $("#answerId").val(json.id);
              $("[name='answer_text']").val(json.answer_text);

              if (json.is_correct === true){
                  $("#id_is_correct").val("True");
              } else {
                $("#id_is_correct'").val("False");
              };
              if (json.is_default === true){
                  $("#id_is_default").val("True");
              } else {
                $("#id_is_default").val("False");
              };
            }
          })
  })
  $(document).on('keyup',"#crudModalDeleteCheckInput", function(){
    if ($("#crudModalDeleteCheckInput").val() === "delete" ){
      $("#crudModalDeleteCheckSubmit").removeClass();
      $("#crudModalDeleteCheckSubmit").addClass("btn");
      $("#crudModalDeleteCheckSubmit").addClass("btn-al");
      $("#crudModalDeleteCheckSubmit").html("Delete");
    } else {
      $("#crudModalDeleteCheckSubmit").removeClass();
      $("#crudModalDeleteCheckSubmit").addClass("btn");
      $("#crudModalDeleteCheckSubmit").addClass("btn-secondary");
      $("#crudModalDeleteCheckSubmit").addClass("disabled");
      $("#crudModalDeleteCheckSubmit").html("type 'delete' to activate");
    }
  })




// When submitting the answer modal perform these functions
  $(document).on('click', "button[id='submitAnswerCrud']", function(event){
      crudModalPost()

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
