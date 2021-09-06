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
      data = JSON.parse(data);
      console.log("benchmarkData", data);
      if(data.length===0) {
        benchmarkQaList.innerHTML = "No questions added yet";
      }else{
        benchmarkQaList.innerHTML = "";
        data.forEach((item) => {
        benchmarkQaList.innerHTML +=`
        <li class="list-group-item">${item.fields.question_text}| ${item.fields.question}</li>`
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
