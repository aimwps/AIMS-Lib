$(document).ready(function(){
  function loadTextEntry(question){
    console.log(question)
    $("#submitSessionAnswer").val("text-entry");
    $("#sessionQuestionId").val(question.id)
    $("#singleChoice").empty()
    $("#multiChoice").empty()
    $("#textEntry").val("")
    $("#textEntryInput").show()
  };

  function loadMultipleChoice(question){
    $("#submitSessionAnswer").val("multiple-choice");
    $("#sessionQuestionId").val(question.id)
    $("#singleChoice").empty()
    $("#multiChoice").empty()
    $("#textEntry").val("")
    $("#textEntryInput").hide()
    $.each(question.answers, function(index, answer){
      $("#singleChoice").append(`
        <li class="list-group-item w-100 border-0">
        <button name="multipleChoiceSelect" value="${answer.id}" class="btn btn-al w-100">${answer.answer_text}</button>
        </li>
        `)
    })
  };
  function loadMultipleCorrectChoice(question){
    console.log(question)
    $("#submitSessionAnswer").val("multiple-correct-choice");
    $("#sessionQuestionId").val(question.id)
    $("#singleChoice").empty()
    $("#multiChoice").empty()
    $("#textEntry").val("")
    $("#textEntryInput").hide()
    $.each(question.answers, function(index, answer){
      $("#singleChoice").append(`
        <li class="list-group-item w-100 border-0">
        <button name="multipleCorrectChoiceSelect" value="${answer.id}" class="btn btn-al w-100">${answer.answer_text}</button>
        </li>
        `)
    }

  };


  function loadSessionQuestion(sessionId){
    console.log(`-----> ${sessionId}`)
    $("#benchmarkSessionModal").modal("show");
    $.ajax({
          method:"GET",
          url:"/BenchmarkView_ajax_get_session_question/",
          datatype:"json",
          data: {session_id : sessionId },
          success: function(json){
            console.log(json)
            let question = json.question;
            $("#questionShow").text(question.question_text)
            if (question.answer_type === "text-entry-exact"){
              loadTextEntryExact(question);
            } else if (question.answer_type === "text-entry-neartest"){
              loadTextEntryNearest(question);
            } else if (question.answer_type === "multiple-choice"){
              loadMultipleChoice(question)
            } else if (question.answer_type === "multiple-correct-choice"){
              loadMultipleCorrectChoice(question)
            } else {
              console.log("question_type_error")
            };
          }});
  };

  $(document).on("click", "[name='multipleChoiceSelect']", function(){
    $("[name='multipleChoiceSelect']").removeClass('active').removeClass('bg-primary');
    $(this).addClass('active').addClass('bg-primary');
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
  $(document).on("click", "#submitSessionAnswer", function(){
    if ($(this).val() === "multiple-choice"){
      console.log("recognised as multiple choice");
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
      $("button[name='multipleCorrectChoiceSelect']").each(function(index, button){
        if ( button.hasClass("active") ){
          multipleCorrectChoiceAnswers.push(button.val())
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
                  text_entry_value: "coming soon",
                },

            datatype:"json",
            success: function(json){
              console.log(json);
            }
      })

    }
  })





})
