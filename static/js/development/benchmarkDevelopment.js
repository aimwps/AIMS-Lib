const qaForm = document.querySelector("#submitQAform");
const searchField = document.querySelector("#searchField");
const benchmarkDev = document.querySelector("#benchmarkDev");
const benchmarkQaList = document.getElementById("benchmarkQaList");
const bquestion = document.getElementById("questionField");
const banswer = document.getElementById("answerField");
const gqbList = document.getElementById("gqbList");
const gqbOutput = document.getElementById("gqbOutput");
const answerModal = document.getElementById("updateAnswerModal");
const answerEditForm = document.getElementById("answerUpdateForm");
const questionEditForm = document.getElementById("questionUpdateForm");


window.onload = function() {
  gqbOutput.style.display="none";
  displayQaList();
};

// FOR SEARCHING GENERATED QUESTIONS BANK.......................................
searchField.addEventListener('keyup', (e) => {
  const searchValue = e.target.value;
  if(searchValue.trim().length>0){
    gqbList.innerHTML = "";
    fetch("/search-generated-questions/", {
      body:JSON.stringify({searchText: searchValue}),
      method:"POST",
    })
    .then((res) => res.json())
    .then((data) => {
      console.log("data", data);
      benchmarkDev.style.display = "none";
      gqbOutput.style.display ="block";
      if(data.length===0) {
        gqbList.innerHTML = "";
        gqbList.innerHTML += `
        <li class="list-group-item">No resaults Found</li>`
      }else{
        gqbList.innerHTML = "";
        data.forEach((item) => {
        gqbList.innerHTML +=`
        <li class="list-group-item">
          <p><strong>Q:</strong> ${item.question}</p>
          <div class="container">
          <p><strong>A:</strong> ${item.answer} <small>[quality: ${item.user_proof}]</small></p>
          </div>
          <a type="button" id="quickAddQuestion${item.id}" onClick="quickSubmitGqb(${item.id})" class="text-primary">
            Add to benchmark
          </a>
          <a type="button" id="addToEditQuestion${item.id}" onClick="editSubmitGqb(${item.id})" class="text-primary">
            Edit before adding
          </a>
          <span style="float:right;"><a type="button" class="text-primary" onClick="clearGqb()">Hide generated questions</a></span>
          </p>
        </li>`
        })
      }
    })
  }else{
    gqbOutput.style.display = "none";
    benchmarkDev.style.display = "block";
  }
});

function clearGqb(){
  $("#searchField").val("");
  gqbOutput.style.display = "none";
  benchmarkDev.style.display = "block";

}
// FOR SUBMITTING A GQB Q&A WITHOUT EDITING
function quickSubmitGqb(gqb_id){
  fetch("/quick-add-gqb-info/", {
    body:JSON.stringify({gqb_id : gqb_id}),
    method: "POST",
  })
  .then((response) => response.json())
  .then((gqb_item) => {
    console.log(gqb_item);
    $('#questionField').val(gqb_item.question);
    $('#answerField').val(gqb_item.answer);
    $('#generatedFromGqbId').val(gqb_item.id);
    submitQA.click();
  });
};

function editSubmitGqb(gqb_id){
  fetch("/quick-add-gqb-info/", {
    body:JSON.stringify({gqb_id : gqb_id}),
    method: "POST",
  })
  .then((response) => response.json())
  .then((gqb_item) => {
    console.log(gqb_item);
    $('#questionField').val(gqb_item.question);
    $('#answerField').val(gqb_item.answer);
    $('#generatedFromGqbId').val(gqb_item.id);
    $('#hasBeenModified').val(1);
    document.getElementById('begin').scrollIntoView();
  });
};

// FOR DISPLAYING THE BENCHMARK Q&A LIST........................................
function displayQaList(){
    $("#questionField").val("");
    $("#answerField").val("");
    $("#generatedFromGqbId").val("");
    $("#hasBeenModified").val("");
    fetch("/display-quiz-dev/", {
      body:JSON.stringify({benchmark_id: $("#onBenchmark").val()}),
      method: "POST",
    })
    .then((response) => response.json())
    .then((data) => {
      console.log("benchmarkData", data);
      if(data.length===0) {
        benchmarkQaList.innerHTML = "No questions added yet";
      }else{
        benchmarkQaList.innerHTML = "";
        data.forEach((item) => {
          benchmarkQaList.innerHTML +=`
          <li class="list-group-item">
          <a type="button" onClick="editQuestion(${item.id})" class="text-primary" data-bs-toggle="modal" data-bs-target="#updateQuestionModal">
            <i class="fas fa-ellipsis-h"></i>
          </a>
          <strong>Q:</strong> ${item.question_text}

          <ul class="list-group list-group-flush" id="qAs${item.id}">`;
          item.answers.forEach((ans) => {
            const innerList = document.getElementById("qAs" + item.id)
            innerList.innerHTML +=`
            <li class="list-group-item">
              <form method="POST">
              <a type="button" onClick="editAnswer(${ans.id})" class="text-primary" data-bs-toggle="modal" data-bs-target="#updateAnswerModal">
                <i class="fas fa-ellipsis-h"></i>
              </a>
              <strong>A: </strong>${ans.answer_text}, <small>correct: ${ans.is_correct}</small>
            </li>
            `;
          })
        benchmarkQaList.innerHTML +=`
        </ul></li>`
      })
    }
  })
};

// FOR SUBMITTING A NEW QUESTION FROM INPUT BOX.................................
qaForm.addEventListener('submit', function(e){
  e.preventDefault();
  $.ajax({
    type:"POST",
    url: "/create-question-answer/",
    data:{
      question:$("#questionField").val(),
      answer:$("#answerField").val(),
      benchmark_id:$("#onBenchmark").val(),
      generated_from:$("#generatedFromGqbId").val(),
      has_been_modified:$("#hasBeenModified").val(),
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
    },
    success: function(){
        displayQaList();
    }
  })
});

// FOR EDITING ANSWERS.........................................................
function editAnswer(answerID){
  fetch("/answer-info/", {
    body:JSON.stringify({answer_id: answerID}),
    method: "POST",
  })
  .then((response) => response.json())
  .then((answer) => {
    $('input[name=answerIdInput]').val(answer.answer.id);
    $('#answerModalAnswerTextInput').val(answer.answer.answer_text);
    $('#answerModalQuestion').text(answer.question);
    $('#answerModalCorrectInput').val(answer.answer.is_correct.toString()).change();

  })
};
answerEditForm.addEventListener('submit', function(e){
  e.preventDefault();
  $.ajax({
    type:"POST",
    url: "/answer-edit/",
    data:{
      answer_id:$('input[name=answerIdInput]').val(),
      answer_text:$("#answerModalAnswerTextInput").val(),
      is_correct:$("#answerModalCorrectInput").val(),
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
    },
    success: function(){
        answerEditSubmit();
    }
  })
});
function answerEditSubmit(){
  $('#updateAnswerModal').modal('toggle');
  displayQaList();
};

// FOR EDITING QUESTIONS.........................................................
function editQuestion(questionId){
  fetch("/question-info/", {
    body:JSON.stringify({question_id: questionId}),
    method: "POST",
  })
  .then((response) => response.json())
  .then((question) => {
    $('input[name=questionIdInput]').val(question.id);
    $('#questionModalQuestionTextInput').val(question.question_text);
    $('#questionModalQuestion').text(question.question_text);
    $('#questionModalAnswerType').val(question.answer_type).change();
  })
};

questionEditForm.addEventListener('submit', function(e){
  e.preventDefault();
  $.ajax({
    type:"POST",
    url: "/question-edit/",
    data:{
      question_id:$('input[name=questionIdInput]').val(),
      question_text:$("#questionModalQuestionTextInput").val(),
      answer_type:$("#questionModalAnswerType").val(),
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
    },
    success: function(){
        questionEditSubmit();
    }
  })
});
function questionEditSubmit(){
  $('#updateQuestionModal').modal('toggle');
  displayQaList();
};

function clearQuick(){
  displayQaList();
}
