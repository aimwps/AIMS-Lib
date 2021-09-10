function getQuestions(){
  $.ajax({
    type:'GET',
    url: "{% url 'get-questions' %}",
    success: function(response){
      console.log(response);
    },
    error: function(response){
      alert("An Error occurec")
    },
  })
}
