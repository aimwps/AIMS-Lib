from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator
USER_STATUS = (('deleted', 'deleted'),
                ('active', 'active'),
                ('inactive', 'inactive'),
                ('completed', 'completed'),)
METRIC_FREQ = (
        ('daily', 'daily'),
        ('weekly', 'weekly'),
        ('monthly', 'monthly'),
        ('yearly', 'yearly'),
)
COMP_CRITERIA = (('consecutive', 'consecutive'),
                ('total', 'total'))

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
    global_standard = models.BooleanField(default=False)

    def __str__(self):
        full_path = [self.title]
        k = self.parent_category
        while k is not None:
            full_path.append(k.title)
            k = k.parent_category
        return ' > '.join(full_path[::-1])
## A user can create many aims
class Aim(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(DevelopmentCategory, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.TextField()
    why = models.TextField(blank=True, null=True)
    user_status = models.CharField(max_length=100, choices=USER_STATUS, default="active")
    def __str__(self):
        return f"<AIM: by {self.user} '{self.title[:min(len(self.title),50)]}'>"#This changes the displayed object name into relevant text information
    def get_absolute_url(self):
        return reverse('aims-dash')

    # def get_aim_trackers(for_user_id):
    #     user_min_aim_trackers = TrackerMinAim.objects.filter(lever__on_aim__user__id=for_user_id)
    #     return ('user_min_aim_trackers', user_min_aim_trackers)
    # def get_daily_trackers(for_user_id):
    #     user_daily_trackers = TrackerMinAim.objects.filter(lever__on_aim__user__id=for_user_id, frequency="daily" )
    #


class Lever(models.Model):
    #tracker = models.ForeignKey(AimsTracker, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(default="A description of the lever you will pull")
    in_order = models.PositiveIntegerField()
    on_aim = models.ForeignKey(Aim, on_delete=models.CASCADE)
    user_status = models.CharField(max_length=100, choices=USER_STATUS, default="active")
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['on_aim', 'in_order'], name='unique order of levers')
        ]

    def get_trackers(self):
        min_aim = list(TrackerMinAim.objects.filter(Q(lever=self)).filter(~Q(user_status="deleted")))
        boolean = list(TrackerBoolean.objects.filter(Q(lever=self)).filter(~Q(user_status="deleted")))
        payload = min_aim+boolean
        sorted_payload = sorted(payload, key=lambda instance: instance.start_date)

        print(sorted_payload)
        return sorted_payload

    def __str__(self):
        return f"<Lever: by {self.on_aim.user} on {self.on_aim} ...'{self.description[:min(len(self.description),50)]}'>"#This changes the displayed object name into relevant text information
    def get_absolute_url(self):
        return reverse('aims-dash')



class TrackerMinAim(models.Model):
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
    user_status = models.CharField(max_length=100, choices=USER_STATUS, default="active")
    # use user week settings
    # use user sleep settings


    def get_tclass(self):
        class_name = "TrackerMinAim"
        return class_name
    def __str__(self):
        return f"<MinAimTracker: {self.frequency}>"#This changes the displayed object name into relevant text information
    def get_absolute_url(self):
        return reverse('aims-dash')

    def get_tsentence(self):

        sentence_start = f"I will show up and {self.metric_description} {self.metric_min} { self.metric_type} "
        if self.frequency_quantity > 1:
            sentence_start += f"{ self.frequency_quantity} times "
        sentence_start +=  f"{self.frequency}. "

        sentence_start+= f"After {self.complete_value} { self.complete_criteria} {self.frequency}  periods of "
        if self.frequency_quantity > 1:
            sentence_start += f"{self.frequency_quantity} * "
        sentence_start +=f"{self.metric_aim} {self.metric_type} I have moved mountains to achieve my aims"
        if self.end_date:
            sentence_start+=f"This tracker is actively trackd until { self.end_date }."
        return sentence_start

    def get_tquestion(self):
        verbose =  {'daily':'today',
                    'weekly': 'this week',
                    'monthly':'this month',
                    'yearly': 'this year'}
        question = f"You aimed to {self.metric_description} {self.metric_min} to {self.metric_aim} {self.metric_type} "
        if self.frequency_quantity > 1:
            question += f"{self.frequency_quantity} times "
        verbose_frequency = verbose[self.frequency]
        question += f"{verbose_frequency}. How did you get on?"
        return question

    def get_pretty_tclass(self):
        class_name = "Minimum show to goal"
        return class_name
class TrackerMinAimRecords(models.Model):
    tracker = models.ForeignKey(TrackerMinAim,on_delete=models.CASCADE)
    lever_performed = models.BooleanField(default=False)
    record_date = models.DateField(auto_now_add=True)
    record_time = models.TimeField(auto_now_add=True)
    metric_quantity  = models.IntegerField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('aims-dash')



##################################################################################################################################
class TrackerBoolean(models.Model):

    # This model is a tracker for completing a recurring lever. The user can set a frequency
    # and will have to complete somewhere between the minimum and the aim.
    lever = models.ForeignKey(Lever,on_delete=models.CASCADE, related_name="tracker_boolean" )
    metric_description = models.TextField(max_length=500) # Represents the amount of minutes I spent jogging today
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
    user_status = models.CharField(max_length=100, choices=USER_STATUS, default="active")

    def get_tclass(self):
        class_name = "TrackerBoolean"
        return class_name
    def __str__(self):
        return f"<TrackerBoolean: {self.frequency}>"#This changes the displayed object name into relevant text information

    def get_absolute_url(self):
        return reverse('aims-dash')

    def get_tsentence(self):
        sentence = f"On a "
        if self.frequency_quantity > 1:
            sentence += f"{self.frequncy_quantity} times "
        sentence += f"{self.frequency} basis; {self.metric_description}"
        return sentence

    def get_pretty_tclass(self):
        class_name = "Yes or no statement"
        return class_name


    def get_tquestion(self):
        x = f'You said; "{self.metric_description}". Are you taking a step forwards?'
        return x

class TrackerBooleanRecords(models.Model):
    tracker = models.ForeignKey(TrackerBoolean,on_delete=models.CASCADE)
    lever_performed = models.BooleanField()
    record_date = models.DateField(auto_now_add=True)
    record_time = models.TimeField(auto_now_add=True)
    metric_quantity  = models.BooleanField(choices=((True,"Yes"), (False, "No")), default="Yes")

    def get_absolute_url(self):
        return reverse('aims-dash')
