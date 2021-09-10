const qaForm = document.querySelector("#submitQAform");
const benchmarkDev = document.querySelector("#benchmarkDev");
const benchmarkQaList = document.getElementById("benchmarkQaList")
const bquestion = document.getElementById("questionField")
const banswer = document.getElementById("answerField")
const searchField = document.querySelector("#searchField");
const gqbOutput = document.querySelector(".gqbOutputView");
const gqbList = document.querySelector(".gqbList");

window.onload = function() {
  displayQaList();
  gqbOutput.style.display = "none";
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
      data = JSON.parse(data);
      console.log("benchmarkData", data);
      if(data.length===0) {
        benchmarkQaList.innerHTML = "No questions added yet";
      }else{
        data.forEach((item) => {
        benchmarkQaList.innerHTML +=`
        <li class="list-group-item">${item.fields.question_text}| ${item.fields.question}</li>`
        })
      }
    })
};
if (ans.is_correct == "True"){
  document.getElementById("trueAnswerOption${ans.id}").prop("checked", true);
}else{
  document.getElementById("falseAnswerOption${ans.id}").prop("checked", true);
};
})

<p class="lead">Answer:</p>
<p>${ans.answer_text}<p>
<p class="lead">Is this answer correct?</p>
<p>${ans.is_correct}</p>
<hr>
<p class="lead">Edit this answer below & update</p>
<p> This is a correct answer:
  <div class="form-check form-check-inline">
    <input class="form-check-input" type="radio" name="answerTrueFalseOption" id="trueAnswerOption${ans.id}" value="option1">
    <label class="form-check-label" for="inlineRadio1">True</label>
  </div>
  <div class="form-check form-check-inline">
    <input class="form-check-input" type="radio" name="answerTrueFalseOption" id="falseAnswerOption${ans.id}" value="option2">
    <label class="form-check-label" for="inlineRadio2">False</label>
  </div>
</p>
</div>




const qaForm = document.querySelector("#submitQAform");
const benchmarkDev = document.querySelector("#benchmarkDev");
const benchmarkQaList = document.getElementById("benchmarkQaList")
const bquestion = document.getElementById("questionField")
const banswer = document.getElementById("answerField")
const gqbList = document.getElementById("gqbList")
const gqbOutput = document.getElementById("gqbOutput")

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
          <li class="list-group-item"><strong>Q:</strong> ${item.question_text}
          <ul class="list-group list-group-flush" id="${item.id}">`
          item.answers.forEach((ans) => {
            const innerList = document.getElementById(item.id)
            innerList.innerHTML +=`
            <li class="list-group-item">
              <div class="row">
                <div class="col-10">
                  <strong>A: </strong>${ans.answer_text}, <small>correct: ${ans.is_correct}</small>
                </div>
                <div class="col-2">
                  <a type="button" class="text-primary" onClick="editAnswer(${ans.id})" data-toggle="modal" data-target="#myModal")"><i class="fas fa-ellipsis-h"></i></a>
                </div>
              </div>
            </li>
            `;

          })
        benchmarkQaList.innerHTML +=`
        </ul></li>`
      })
    }
  })
};


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
const answerDeleteForm = document.querySelector("#answerDeleteForm")
answerDeleteForm.addEventListener('submit', function(e){
  e.preventDefault();
  $.ajax({
    type:"POST",
    url: "/answer-delete/",
    data:{
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
    },
    success: function(){
        displayQaList();
    }
  })
});

function editAnswer(event, register_id) {
    var modal = $('#modal_register_edit');
    var url = $(event.target).closest('a').attr('href');
    modal.find('.modal-body').html('').load(url, function() {
        modal.modal('show');
        formAjaxSubmit(popup, url);
    });
}
