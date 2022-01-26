$(document).ready(function(){
  function loadTextEntry(sessionQuestion){
    $("#submitSessionAnswer").val("text-entry");
    $("#sessionQuestionId").val(sessionQuestion.id)
    $("#singleChoice").empty()
    $("#multiChoice").empty()
    $("#textEntry").val("")
    $("#textEntryInput").show()
  };

  function loadMultipleChoice(sessionQuestion){
    $("#submitSessionAnswer").val("multiple-choice");
    $("#sessionQuestionId").val(sessionQuestion.id)
    $("#singleChoice").empty()
    $("#multiChoice").empty()
    $("#textEntry").val("")
    $("#textEntryInput").hide()
    $.each(sessionQuestion.question.answers, function(index, answer){
      $("#singleChoice").append(`
        <li class="list-group-item w-100 border-0">
        <button name="multipleChoiceSelect" value="${answer.id}" class="btn btn-al w-100">${answer.answer_text}</button>
        </li>
        `)
    })
  };
  function loadMultipleCorrectChoice(sessionQuestion){
    console.log(sessionQuestion)
    $("#submitSessionAnswer").val("multiple-correct-choice");
    $("#sessionQuestionId").val(sessionQuestion.id)
    $("#singleChoice").empty()
    $("#multiChoice").empty()
    $("#textEntry").val("")
    $("#textEntryInput").hide()
    $.each(sessionQuestion.question.answers, function(index, answer){
      $("#numCorrectAnswers").val(sessionQuestion.question.num_correct_answers)
      $("#singleChoice").append(`
        <li class="list-group-item w-100 border-0">
        <button name="multipleCorrectChoiceSelect" value="${answer.id}" class="btn btn-al w-100">${answer.answer_text}</button>
        </li>
        `)
    })

  };


  function loadSessionQuestion(sessionId){
    console.log(`-----> ${sessionId}`)
    $("#submitSessionAnswer").addClass("disabled")
    $("#benchmarkSessionModal").modal("show");
    $.ajax({
          method:"GET",
          url:"/BenchmarkView_ajax_get_session_question/",
          datatype:"json",
          data: {session_id : sessionId },
          success: function(json){
            console.log("session",json)
            let question = json.question;
            $("#questionShow").text(question.question_text)
            $("#currenSessionTotalQuestions").text(question.total_session_answers)

            if (question.answer_type === "text-entry-exact"){
              loadTextEntry(json);
              $("#questionType").text("Enter the exact answer with correct grammar, spelling, capitalisation and punctuation")
            } else if(question.answer_type ===  "text-entry-nearest" ){
              loadTextEntry(json);
              $("#questionType").text("Enter an answer, we'll help you out with grammar, spelling, capitalisation and punctuation")
            } else if (question.answer_type === "multiple-choice"){
              $("#questionType").text("Select a single answer")
              loadMultipleChoice(json)
            } else if (question.answer_type === "multiple-correct-choice"){
              let verbose = (question.num_correct_answers > 1) ? "answers":"answer";
              $("#questionType").text(`Select ${question.num_correct_answers} ${verbose}`)
              loadMultipleCorrectChoice(json)
            } else {
              console.log("question_type_error")
            };
          }});
  };

$(document).on("keyup", "#textEntryInput", function(){
  if ( $(this).val().length > 0 ){
    $("#submitSessionAnswer").removeClass("disabled")
  } else {
    $("#submitSessionAnswer").addClass("disabled")
  }
})

  $(document).on("click", "[name='multipleChoiceSelect']", function(){
    $("[name='multipleChoiceSelect']").removeClass('active').removeClass('bg-primary');
    $(this).addClass('active').addClass('bg-primary');
    $("#submitSessionAnswer").removeClass("disabled")

  })
  $(document).on("click", "#newSessionBtn", function(){

    $.ajax({
      method: "GET",
      url: "/BenchmarkView_ajax_get_new_session/",
      data: {benchmark_id: $("#benchmarkId").val()},
      datatype:"json",
      success: function(json){
        console.log(json)
        loadSessionQuestion(json.session_id)
      }
    })
  });

  $(document).on("click", "[name='multipleCorrectChoiceSelect']", function(e){
    e.preventDefault();
    if( $(this).hasClass("active") ){
      $(this).removeClass("active");
      $(this).removeClass("bg-primary").addClass("bg-white");
    } else {
      $(this).addClass("active");
      $(this).removeClass("bg-white").addClass("bg-primary");
    };

    let currentActive = 0;
    console.log(currentActive, parseInt( $("#numCorrectAnswers").val() ) )
    $("[name='multipleCorrectChoiceSelect']").each(
      function(){
        if( $(this).hasClass("active") ){
          currentActive += 1;
        }
      }
    );

    if ( currentActive === parseInt($("#numCorrectAnswers").val()) ){
      $("#submitSessionAnswer").removeClass("disabled");
      $("[name='multipleCorrectChoiceSelect']").each( function(){
        if ( !$(this).hasClass("active") ){
          $(this).addClass("disabled")
        }
      })

    } else {
      $("#submitSessionAnswer").addClass("disabled")
      $("[name='multipleCorrectChoiceSelect']").each( function(){
          $(this).removeClass("disabled")
        }
      )
    }


  })
  $(document).on("click", "#submitSessionAnswer", function(){

      let multipleChoiceAnswers = [];
      let multipleCorrectChoiceAnswers = [];

      // Get any multiple choice answers selected
      $("button[name='multipleChoiceSelect']").each( function(){
        console.log($(this).val())
        if ( $(this).hasClass("active") ){
          multipleChoiceAnswers.push($(this).val())
        };
      });
      // Get any multiple correct choice answers selected
      $("button[name='multipleCorrectChoiceSelect']").each(function(){
        if ( $(this).hasClass("active") ){
          multipleCorrectChoiceAnswers.push($(this).val())
        };
      });

      $.ajax({
            method:"POST",
            url: "/BenchmarkView_ajax_submit_answer/",
            data: {
                  question_type: $("#submitSessionAnswer").val(),
                  session_question_id: $("#sessionQuestionId").val(),
                  csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                  multiple_choice_value: multipleChoiceAnswers,
                  multiple_correct_choice_values: multipleCorrectChoiceAnswers,
                  text_entry_value: $("#textEntryInput").val(),
                },

            datatype:"json",
            success: function(json){
              console.log(json);
              loadSessionQuestion(json.session_id)
            }
      })
    })
});
