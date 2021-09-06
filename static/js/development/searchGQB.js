searchField.addEventListener('keyup', (e) => {
  const searchValue = e.target.value;
  if(searchValue.trim().length>0){
    gqbList.innerHTML = " ";
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
        gqbOutput.innerHTML = "No results found";
      }else{
        data.forEach((item) => {
        gqbList.innerHTML +=`
        <li class="list-group-item">${item.question}, ${item.answer}, ${item.id}, ${item.user_proof}</li>`
        })
      }
    })
  }else{
    gqbOutput.style.display = "none";
    benchmarkDev.style.display = "block";

  }
})
