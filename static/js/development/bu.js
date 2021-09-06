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
