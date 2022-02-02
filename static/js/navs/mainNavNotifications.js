$(document).ready(function (){
  // var intervalChecker =  setInterval(checkNavBarNotifications, 5000);
  function checkGQBstatus(){
    $.ajax({url: "/check-gqb-status/",
            type: "GET",
            success: function(response){
              var textLink = '<a class="nav-link active" href="/verify-gqb/">['+response.gqb_quantity+' ready to verify]</a>'
              if(response.gqb_quantity > 0){
                $('#verifyQAGstatus').html(textLink)
              }else{
                $('#verifyQAGstatus').empty();
              };
            }})
  }
  function checkOrganisationInvites(){
    $.ajax({
      type: "GET",
      url:"/nav_ajax_check_organisation_invites/",
      datatype: 'json',
      success: function(json){

        if (json.length > 0){

        $("#pathwayNotifcations").append(`<i class="fas fa-route"></i>`)
      }
// Set the sub nav notification
// return the length for main nav notification
      }
    })
  }
  function checkPathwayInvites(){
    $.ajax({
      type: "GET",
      url:"/nav_ajax_check_pathway_invites/",
      datatype: 'json',
      success: function(json){
        console.log(json)
        // Set the sub nav notification
        $("#pathwayNotifcations").append(`<i class="fas fa-route"></i>`)
        // return the length for main nav notification
      }
    })
  }

  function checkNavBarNotifications(){
    console.log("check Performed");
    let pathwayNotifcations = checkPathwayInvites();
    let organisationNotifcaitons = checkOrganisationInvites();

  }


});
