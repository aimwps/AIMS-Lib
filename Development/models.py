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
            models.UniqueConstraint(fields=['author', 'order_positon'], name='unique_order_of_aims')
        ]
    def __str__(self):
        return f"Aim_{self.id}"

    def get_absolute_url(self):
        return reverse('aims-dash')


class Behaviour(models.Model):
    title = models.TextField()
    on_aim = models.ForeignKey(Aim, on_delete=models.CASCADE)
    user_status = models.CharField(max_length=100, choices=USER_STATUS, default="active")
    order_positon = models.PositiveIntegerField()
    create_date = models.DateField(auto_now_add=True, blank=True, null=True)
    create_time = models.TimeField(auto_now_add=True, blank=True, null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['on_aim', 'order_position'], name='unique_order_of_behaviours')
        ]

    def get_trackers(self):
        return []

    def __str__(self):
        return f"Behaviour_{self.id}"
    def get_absolute_url(self):
        return reverse('aims-dash')

class StepTracker(models.Model):
    on_behaviour = models.ForeignKey(Behaviour,on_delete=models.CASCADE, related_name="trackers")
    metric_tracker_type =  models.CharField(max_length=100, choices=TRACKER_TYPE)
    metric_action = models.TextField(blank=True, null=True)
    metric_unit = models.CharField(max_length=100)
    metric_number_display_type = models.CharField(max_length=100, choices=NUMBER_TYPE)
    metric_min = models.FloatField()
    metric_max = models.FloatField()
    minimum_show_allowed = models.BooleanField()
    minimum_show_description = models.TextField(blank=True, null=True)
    #record_type = models.CharField(max_length=100,choices=METRIC_FREQ)
    record_start_date = models.TimeField(auto_now_add=True, blank=True, null=True)
    record_frequency = models.CharField(max_length=100,choices=RECORD_FREQUENCY)
    record_multiple_per_frequency = models.BooleanField()
    complete_criteria =  models.CharField(max_length=100, choices=COMP_CRITERIA)
    complete_value = models.PositiveIntegerField()
    user_status = models.CharField(max_length=100, choices=USER_STATUS, default="active")
    order_positon = models.PositiveIntegerField()
    create_date = models.DateField(auto_now_add=True, blank=True, null=True)
    create_time = models.TimeField(auto_now_add=True, blank=True, null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['on_behaviour', 'order_position'], name='unique_order_of_trackers')
        ]
    def __str__(self):
        return f"StepTracker_{self.id}"
