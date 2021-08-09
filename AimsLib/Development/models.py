from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator



class SkillArea(models.Model):
    skill_area_name = models.CharField(max_length=255)
    created_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    forum_rules = models.TextField(default="The forum rules for this skill area are..")
    def __str__(self):
        return self.skill_area_name #This changes the displayed object name into relevant text information

## Base include 'Health', 'Mind Set', 'Skills'
class DevelopmentCategory(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    parent_category = models.ForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.SET_NULL)
    def __str__(self):
        return f"<DevCat: {self.title}>" #This changes the displayed object name into relevant text information


## A user can create many aims
class Aim(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(DevelopmentCategory, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    why = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"<AIM: by {self.user} '{self.title[:min(len(self.title),50)]}'>"#This changes the displayed object name into relevant text information
    def get_absolute_url(self):
        return reverse('aims-dash')

    def get_aim_trackers(for_user_id):
        user_min_aim_trackers = TrackerMinAim.objects.filter(lever__on_aim__user__id=for_user_id)
        return ('user_min_aim_trackers', user_min_aim_trackers)
    def get_daily_trackers(for_user_id):
        user_daily_trackers = TrackerMinAim.objects.filter(lever__on_aim__user__id=for_user_id, frequency="daily" )



class Lever(models.Model):
    #tracker = models.ForeignKey(AimsTracker, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(default="A description of the lever you will pull")
    in_order = models.PositiveIntegerField()
    on_aim = models.ForeignKey(Aim, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['on_aim', 'in_order'], name='unique order of levers')
        ]

    def get_trackers(self):
        min_aim = TrackerMinAim.objects.filter(Q(lever=self))
        return min_aim

    def __str__(self):
        return f"<Lever: by {self.on_aim.user} on {self.on_aim} ...'{self.description[:min(len(self.description),50)]}'>"#This changes the displayed object name into relevant text information
    def get_absolute_url(self):
        return reverse('aims-dash')



class TrackerMinAim(models.Model):
    METRIC_FREQ = (
            ('daily', 'daily'),
            ('weekly', 'weekly'),
            ('monthly', 'monthly'),
            ('yearly', 'yearly'),
    )
    COMP_CRITERIA = (('consecutive', 'consecutive'),
                    ('total', 'total'))

    TIMEOUT_FREQUENCY = (
                    ("double frequency","double frequency"),
                    ("weekly mondays","weekly mondays"),
                    ("weekly tuesdays","weekly tuesdays"),
                    ("weekly wednesdays","weekly wednesdays"),
                    ("weekly thursdays","weekly thursdays"),
                    ("weekly fridays","weekly fridays"),
                    ("weekly saturdays","weekly saturdays"),
                    ("weekly sundays","weekly sundays")
                        )
    WEEK_RESET_CHOICES = (
                    ("start date day", "The day of the week you start your tracker"),
                    ("members profile", "The day set on your user profile")
                    )
    DAY_RESET_CHOICES = (
                    ("midnight", "midnight"),
                    ("sleep setting", "your sleep setting")
                    )
    # This model is a tracker for completing a recurring lever. The user can set a frequency
    # and will have to complete somewhere between the minimum and the aim.
    lever = models.ForeignKey(Lever,on_delete=models.CASCADE, related_name="tracker_min_aim" )
    metric_type = models.CharField(max_length=100) # A description of what the intgers mean. hours, #reps, #minutes #count
    metric_min = models.PositiveIntegerField()# The minimum amount accepted
    metric_aim = models.PositiveIntegerField() # The standard you are trying to hit each day: "8 hours"
    metric_description = models.TextField(blank=True, null=True) # Represents the amount of minutes I spent jogging today
    frequency = models.CharField(max_length=100,choices=METRIC_FREQ) # Choi
    frequency_quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    start_date = models.DateField() # Auto adds today or user can set the first day to start on.
    end_date = models.DateField(blank=True, null=True) # If blank the Tracker runs forever.
    complete_criteria =  models.CharField(max_length=100, choices=COMP_CRITERIA)
    complete_value = models.PositiveIntegerField()
    has_prompt = models.BooleanField(default=True)
    has_timeout = models.BooleanField(default=True)
    has_public_logs = models.BooleanField(default=False)
    allows_multi_period_logs = models.BooleanField(default=True)
    week_reset_on = models.CharField(max_length=100, choices=WEEK_RESET_CHOICES, default="start date day")
    day_reset_on = models.CharField(max_length=100, choices=DAY_RESET_CHOICES, default="midnight")
    # use user week settings
    # use user sleep settings


    def get_tclass(self):
        class_name = "TrackerMinAim"
        return class_name
    def __str__(self):
        return f"<MinAimTracker: {self.frequency}>"#This changes the displayed object name into relevant text information
    def get_absolute_url(self):
        return reverse('aims-dash')

class MinAimRecords(models.Model):
    tracker = models.ForeignKey(TrackerMinAim,on_delete=models.CASCADE)
    lever_performed = models.BooleanField()
    record_date = models.DateField(auto_now_add=True)
    record_time = models.TimeField(auto_now_add=True)
    metric_quantity  = models.IntegerField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('aims-dash')

# class AimTrackers(models.Model):
#     pass





# class TrackerActionRating(models.Model):
#     # This model is a tracker for completing a recurring lever. The user can set a frequency
#     # and provide a description of what ratings mean. e.g. 0-nothing was good about my diet today, 1-i cheated 2/3 meals. 2-I was moderately pleased with my diet today. 3-It was almost perfect. 4- My body loves me after the perfect diet today.
#     metric_type = ""  # A string description of what the intgers mean for each number from metric_min to metric_max
#     metric_min = "" # The minimum rating number
#     metric_max = "" # the maximum rating number
#     description = ""  # This tracker rates my actions in regards to my aim of eating whole foods.
#     frequency = ""
#     start_date = ""
#     end_date = ""
#
#
# class TrackerBoolean(models.Model):
#     description = "" # ""
#     frequency = ""
#     start_date = ""
#     end_date = ""





# Aims & Levers can all be tracked with a tracker.
# class AimsTracker(models.Model):
#     user = ''
#     frequency = ''
#     og_start_date = ''
#     tracker_type = '' # Reduction, # Expansion, # Finite, # Infinite
#
#


    # has categor
    # Description
    # Title
    # Milestones
    # Trackers
    #

# class trainingArticle(models.Model):
#     article_title = models.CharField(max_length=255)
#
