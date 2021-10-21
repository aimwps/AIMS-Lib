$(document).ready(function(){
  $('#id_record_log_length').on('change', function() {
    console.log(this.value)
    if ( this.value == 'day')
    {
      $('#id_record_frequency option[value="daily"]').removeAttr("disabled");
      $('#id_record_frequency option[value="daily"]').attr("selected","selected");
      $('#id_record_frequency option[value="weekly"]').attr("disabled", "disabled").removeAttr("selected");
      $('#id_record_frequency option[value="monthly"]').attr("disabled", "disabled").removeAttr("selected");
      $('#id_record_frequency option[value="yearly"]').attr("disabled", "disabled").removeAttr("selected");
      $('#id_record_frequency option[value="custom"]').removeAttr("disabled").removeAttr("selected");
      $("#CustomDayDates").show();
      $("#CustomWeekDays").show();
      $("#CustomMonths").hide();

    } else if (this.value =='week')
    {
      $('#id_record_frequency option[value="daily"]').attr("disabled", "disabled").removeAttr("selected");
      $('#id_record_frequency option[value="weekly"]').removeAttr("disabled");
      $('#id_record_frequency option[value="weekly"]').attr("selected","selected");
      $('#id_record_frequency option[value="monthly"]').attr("disabled", "disabled").removeAttr("selected");
      $('#id_record_frequency option[value="yearly"]').attr("disabled", "disabled").removeAttr("selected");
      $('#id_record_frequency option[value="custom"]').removeAttr("disabled").removeAttr("selected");
      $("#CustomDayDates").hide();
      $("#CustomWeekDays").hide();
      $("#CustomMonths").hide();
    } else if (this.value =='month')
    {
      $('#id_record_frequency option[value="daily"]').attr("disabled", "disabled").removeAttr("selected");
      $('#id_record_frequency option[value="weekly"]').attr("disabled", "disabled").removeAttr("selected");
      $('#id_record_frequency option[value="monthly"]').removeAttr("disabled");
      $('#id_record_frequency option[value="monthly"]').attr("selected","selected");
      $('#id_record_frequency option[value="yearly"]').attr("disabled", "disabled").removeAttr("selected");
      $('#id_record_frequency option[value="custom"]').removeAttr("disabled").removeAttr("selected");
      $("#CustomDayDates").hide();
      $("#CustomWeekDays").hide();
      $("#CustomMonths").show();
    } else if (this.value =='year')
    {
      $('#id_record_frequency option[value="daily"]').attr("disabled", "disabled");
      $('#id_record_frequency option[value="weekly"]').attr("disabled", "disabled");
      $('#id_record_frequency option[value="monthly"]').attr("disabled", "disabled");
      $('#id_record_frequency option[value="yearly"]').removeAttr("disabled");
      $('#id_record_frequency option[value="yearly"]').attr("selected","selected");
      $('#id_record_frequency option[value="custom"]').attr("disabled", "disabled");
      $("#CustomFrequencyEntry").hide();
    }
    else {
      console.log("Errorrrrrrrrrrr")
      $('#id_record_frequency option[value="daily"]').removeAttr("disabled");
      $('#id_record_frequency option[value="weekly"]').removeAttr("disabled");
      $('#id_record_frequency option[value="monthly"]').removeAttr("disabled");
      $('#id_record_frequency option[value="yearly"]').removeAttr("disabled");
      $('#id_record_frequency option[value="custom"]').removeAttr("disabled");
      $("#CustomFrequencyEntry").hide();
    }
  });
    $('#id_record_frequency').on('change', function() {
      if ( this.value == 'custom')
      {
        $("#CustomFrequencyEntry").show();
      }
      else
      {
        $("#CustomFrequencyEntry").hide();
      }
    });
    $('#id_metric_tracker_type').on('change', function() {
      if ( this.value == 'boolean')
      {
        $("#unit_measurement").hide();
        $("#minimum_expectation").hide();
        $("#max_expectation").hide();
        $("#whole_numbers").hide();
        $("#multiple_records").hide();
      }
      else
      {
        $("#unit_measurement").show();
        $("#minimum_expectation").show();
        $("#max_expectation").show();
        $("#whole_numbers").show();
        $("#multiple_records").show();
      }
    });
    $('#id_minimum_show_allowed').on('change', function() {
      if ( this.checked)
      {
        $("#show_up_dec").show();
      }
      else
      {
        $("#show_up_dec").hide();
      }
    });
    $('#id_complete_allowed').on('change', function() {
      if ( this.checked)
      {
        $("#milestone_crtieria").show();
        $("#milestone_quantity").show();
      }
      else
      {
        $("#milestone_crtieria").hide();
        $("#milestone_quantity").hide();
      }
    });
});
