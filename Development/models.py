from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator
from WebsiteTools.models import ContentCategory
USER_STATUS =   (('deleted', 'deleted'),
                ('active', 'active'),
                ('inactive', 'inactive'),
                ('completed', 'completed'),
                )
RECORD_FREQUENCY =(('daily', 'daily'),
                ('weekly', 'weekly'),
                ('monthly', 'monthly'),
                ('yearly', 'yearly'),
                ('custom', 'custom'),
                )
COMP_CRITERIA = (('consecutive', 'consecutive'),
                ('total', 'total'))

TRACKER_TYPE = (('maximize', 'Count Up'),
                ('minimize', 'Count Down'),
                ('boolean', 'Yes or No'),
                )
NUMBER_TYPE = (('float', 'Upto 2 decimal places'),
                ('integer', 'Whole number only'),
                )


class Aim(models.Model):
    title = models.TextField()
    motivation = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ContentCategory, blank=True, null=True, on_delete=models.SET_NULL)
    user_status = models.CharField(max_length=100, choices=USER_STATUS, default="active")
    order_position = models.PositiveIntegerField(default=9999)
    create_date = models.DateField(auto_now_add=True, blank=True, null=True)
    create_time = models.TimeField(auto_now_add=True, blank=True, null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'order_position'], name='unique_order_of_aims')
        ]
    def __str__(self):
        return f"Aim_{self.id}"

    def get_absolute_url(self):
        return reverse('aims-dash')


class Behaviour(models.Model):
    title = models.TextField()
    on_aim = models.ForeignKey(Aim, on_delete=models.CASCADE)
    user_status = models.CharField(max_length=100, choices=USER_STATUS, default="active")
    order_position = models.PositiveIntegerField()
    create_date = models.DateField(auto_now_add=True, blank=True, null=True)
    create_time = models.TimeField(auto_now_add=True, blank=True, null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['on_aim', 'order_position'], name='unique_order_of_behaviours')
        ]

    def __str__(self):
        return f"Behaviour_{self.id}"
    def get_absolute_url(self):
        return reverse('aims-dash')

class StepTracker(models.Model):
    on_behaviour = models.ForeignKey(Behaviour,on_delete=models.CASCADE, related_name="trackers")
    metric_tracker_type =  models.CharField(max_length=100, choices=TRACKER_TYPE)
    metric_action = models.TextField(blank=True, null=True)
    metric_unit = models.CharField(max_length=100, blank=True, null=True)
    metric_int_only = models.BooleanField(blank=True, null=True)
    metric_min = models.FloatField(blank=True, null=True)
    metric_max = models.FloatField(blank=True, null=True)
    minimum_show_allowed = models.BooleanField(blank=True, null=True)
    minimum_show_description = models.TextField(blank=True, null=True)
    record_start_date = models.DateField(auto_now_add=False)
    record_frequency = models.CharField(max_length=100,choices=RECORD_FREQUENCY)
    record_multiple_per_frequency = models.BooleanField()
    complete_allowed = models.BooleanField(default=True)
    complete_criteria =  models.CharField(max_length=100, choices=COMP_CRITERIA, default="consecutive")
    complete_value = models.PositiveIntegerField()
    user_status = models.CharField(max_length=100, choices=USER_STATUS, default="active")
    order_position = models.PositiveIntegerField(default=9999)
    create_date = models.DateField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['on_behaviour', 'order_position'], name='unique_order_of_trackers')
        ]
    def __str__(self):
        return f"StepTracker_{self.id}"

    def get_tsentence(self):
        tsentence = ""
        if self.metric_int_only:
            metric_min = int(round(self.metric_min, 0))
            metric_max = int(round(self.metric_max, 0))
        if self.metric_tracker_type == "boolean":
            tsentence += f"{self.metric_action}. "
        if self.metric_tracker_type == "maximize":
            period = f"Each {self.record_frequency} period"
            action_min = f"I {self.metric_action} a minimum {metric_min} {self.metric_unit}. "
            action_max = f"I take steps towards achieving {metric_max} {self.metric_unit}. "
            tsentence += "".join([period, action_min, action_max])
        if self.metric_tracker_type == "minimize":
            period = f"Each {self.record_frequency} period"
            action_min = f"I {self.metric_action} a maximum {metric_min} {self.metric_unit}. "
            action_max = f"I take steps towards achieving {metric_max} {self.metric_unit}. "
            tsentence += " ".join([period, action_min, action_max])

        return tsentence

    def get_tquestion(self):
        return  self.get_tsentence() + " How did you get on?"
    def get_milestone_sentence(self):
        period_words = {"daily": "days", "weekly": "weeks", "monthly": "months", "yearly": "years"}
        sentence = ""
        if self.complete_allowed:
            value = str(self.complete_value)
            criteria = str(self.complete_criteria)
            period = period_words[self.record_frequency]
            sentence += " ".join([value, criteria, period])
        else:
            sentence += "No milestone set"
        return sentence

class StepTrackerLogs(models.Model):
    TRACKER_LOG_TYPE = (
                        ("count_showup","count show up"),
                        ("count_value","count submit"),
                        ("boolean_showup", "boolean show up"),
                        ("boolean_success", "boolean complete"),
                        ("fail_or_no_submit","fail or no submit"),
                        )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    on_tracker = models.ForeignKey(StepTracker, on_delete=models.CASCADE, related_name="tracker_logs")
    create_date = models.DateField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)
    submit_type = models.CharField(max_length=100, choices=TRACKER_LOG_TYPE)
    count_value = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"TrackerLog_{self.id}"
