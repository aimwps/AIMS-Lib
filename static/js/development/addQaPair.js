const qaForm = document.querySelector("#submitQAform");
const benchmarkDev = document.querySelector("#benchmarkDev");
const benchmarkQaList = document.getElementById("benchmarkQaList")
const bquestion = document.getElementById("questionField")
const banswer = document.getElementById("answerField")
const gqbList = document.getElementById("gqbList")
const gqbOutput = document.getElementById("gqbOutput")
const answerModal = document.getElementById("answerModal")
const questionTable = document.getElementById("questionTable")

window.onload = function() {
  gqbOutput.style.display="none";
  displayQaList();
};



function displayQaList(){
    banswer.value = "";
    bquestion.value = "";
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

function editAnswer(answerID){
  fetch("/answer-info/", {
    body:JSON.stringify({answer_id: answerID}),
    method: "POST",
  })
  .then((response) => response.json())
  .then((answer) => {
    console.log(answer.is_correct)
    $('#answerModalAnswerTextInput').val(answer.answer_text);
    $('#answerModalCorrectInput').val(answer.is_correct.toString()).change();
  })

  }



qaForm.addEventListener('submit', function(e){
  e.preventDefault();
  $.ajax({
    type:"POST",
    url: "/create-question-answer/",
    data:{
      question:$("#questionField").val(),
      answer:$("#answerField").val(),
      benchmark_id:$("#onBenchmark").val(),
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
    },
    success: function(){
        displayQaList();
    }
  })
});
