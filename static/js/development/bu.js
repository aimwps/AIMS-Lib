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
