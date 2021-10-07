$(document).ready(function(){
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
