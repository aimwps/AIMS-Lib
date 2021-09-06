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
                  <a type="button" href='#' data-bs-toggle="modal" data-bs-target="#answerModal${ans.id}"><i class="fas fa-ellipsis-h"></i></a>
                </div>
              </div>
              <!-- Answer Settings Modal -->
              <div class="modal fade" id="answerModal${ans.id}" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="answerModal${ans.id}Label" aria-hidden="true">
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title" id="answerModal${ans.id}Label">Answer Settings</h5>
                      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                    <p class="lead">Question:</p>
                    <p>${item.question_text}</p>
                    <form action="." method="POST">
                      <textarea type="text" class="form-control" id="answerTextEdit" rows=3>${ans.answer_text}</textarea>
                      <br>
                      <div class="row">
                        <div class="col-4 mt-2">
                          Marked as correct:
                        </div>
                        <div class="col-8">
                          <select class="form-select" aria-label="trueFalseSelect" value="${ans.is_correct}">
                            <option value="True">true</option>
                            <option value="False">false</option>
                          </select>
                        </div>
                      </div>
                    <br>
                    <div class="modal-footer">
                    <button value="${ans.id}" class="btn btn-primary">Update</button>
                      </form>
                      <form id="#answerDeleteForm" method="POST">
                        <button type="submit" value="${ans.id}" class="btn btn-secondary">
                          <i class="far fa-trash-alt"></i></button>
                      </form>
                    </div>
                  </div>
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
