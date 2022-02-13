from rest_framework import serializers
from .models import StepTracker, Aim, Behaviour


class BehaviourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Behaviour
        fields = ("id", "title",)

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
                )
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
              "record_multiple_per_frequency",
              "record_verification_date",
              "complete_allowed",
              "complete_criteria",
              "complete_value",
              "user_status",
              "order_position",
              "create_date",
              "create_time",
                  )
