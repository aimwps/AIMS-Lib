from rest_framework import serializers
from .models import StepTracker, Aim, Behaviour



class StepTrackerSerializer(serializers.ModelSerializer):
    class Meta:
      model = StepTracker
      fields = ("id","on_behaviour",
              "metric_tracker_type",
              "metric_action",
              "metric_unit",
              "metric_int_only",
              "metric_min",
              "metric_max",
              "minimum_show_allowed",
              "minimum_show_description",
              "record_start_date",
              "record_frequency",
              "record_log_length",
              "record_multiple_per_frequency",
              "record_verification_date",
              "complete_allowed",
              "complete_criteria",
              "complete_value",
              "user_status",
              "order_position",
              "create_date",
              "create_time",
              "get_tsentence",
              "library_type",
              "library_title",
              "library_description",
              "get_type_sentence",
              "get_frequency_sentence"
                  )
class BehaviourSerializer(serializers.ModelSerializer):
    trackers = StepTrackerSerializer(many=True)
    class Meta:
        model = Behaviour
        fields = ("id", "title","trackers","library_type","library_title","library_description", )

class AimLibrarySerializer(serializers.ModelSerializer):
    behaviours  = BehaviourSerializer(many=True)
    class Meta:
        model = Aim
        fields = (
                "id",
                "title",
                "motivation",
                "category",
                "create_date",
                "create_time",
                "behaviours",
                "library_type",
                "library_description",
                "library_title"
                )
