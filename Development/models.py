from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator
from WebsiteTools.models import ContentCategory
from django.utils.timezone import now
import pandas as pd
USER_STATUS =   (('deleted', 'deleted'),
                ('active', 'active'),
                ('inactive', 'inactive'),
                ('completed', 'completed'),
                )
RECORD_FREQUENCY =(
                    ('daily', 'Every day'),
                    ('weekly', 'Every week'),
                    ('monthly', 'Every month'),
                    ('yearly', 'Every year'),
                    ('custom', 'Specific days, weeks or months'),
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
CUSTOM_LOG_CODES =[
            ("Day repeat",
                        (
                            ("Monday", "Monday"),
                            ("Tuesday", "Tuesday"),
                            ("Wednesday", "Wendnesday"),
                            ("Thursday", "Thursday"),
                            ("Friday", "Friday"),
                            ("Saturday", "Saturday"),
                            ("Sunday", "Sunday")
                        )
            ),
            ("Day of month repeat",
                        (
                            ("1", 1),
                            ("2", 2),
                            ("3", 3),
                            ("4", 4),
                            ("5", 5),
                            ("6", 6),
                            ("7", 7),
                            ("8", 8),
                            ("9", 9),
                            ("10", 10),
                            ("11", 11),
                            ("12", 12),
                            ("13", 13),
                            ("14", 14),
                            ("15", 15),
                            ("16", 16),
                            ("17", 17),
                            ("18", 18),
                            ("19", 19),
                            ("20", 20),
                            ("21", 21),
                            ("22", 22),
                            ("23", 23),
                            ("24", 24),
                            ("25", 25),
                            ("26", 26),
                            ("27", 27),
                            ("28", 28),
                            ("29", 29),
                            ("30", 30),
                            ("31", 31),
                            ("last_day", "Last day in month")
                        )
            ),
            ("Month of year repeat",
                        (
                            ("January", "January"),
                            ("February", "February"),
                            ("March", "March"),
                            ("April", "April"),
                            ("May", "May"),
                            ("June", "June"),
                            ("July", "July"),
                            ("August", "August"),
                            ("September", "September"),
                            ("October", "October"),
                            ("November", "November"),
                            ("December", "December")
                        )
            )]
LOG_LENGTH = (("day", "A day"),
            ("week", "A week"),
            ("month", "A month"),
            ("year", "A year"))

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
    metric_tracker_type =  models.CharField(max_length=100, choices=TRACKER_TYPE, default="boolean")
    metric_action = models.TextField(blank=True, null=True)
    metric_unit = models.CharField(max_length=100, blank=True, null=True)
    metric_int_only = models.BooleanField(blank=True, null=True)
    metric_min = models.FloatField(blank=True, null=True)
    metric_max = models.FloatField(blank=True, null=True)
    minimum_show_allowed = models.BooleanField(blank=True, null=True)
    minimum_show_description = models.TextField(blank=True, null=True)
    record_start_date = models.DateField(auto_now_add=False)
    record_frequency = models.CharField(max_length=100,choices=RECORD_FREQUENCY, default="weekly")
    record_log_length = models.CharField(max_length=100, choices=LOG_LENGTH, default="day")
    record_multiple_per_frequency = models.BooleanField()
    record_verification_date = models.DateTimeField(blank=True, null=True)
    complete_allowed = models.BooleanField(default=False)
    complete_criteria =  models.CharField(max_length=100, choices=COMP_CRITERIA, default="consecutive")
    complete_value = models.PositiveIntegerField(blank=True, null=True)
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
            period = f"Each {self.record_frequency} period.. "
            action_min = f"I {self.metric_action} a minimum {self.metric_min} {self.metric_unit}. "
            action_max = f"I take steps towards achieving {self.metric_max} {self.metric_unit}. "
            tsentence += "".join([period, action_min, action_max])
        if self.metric_tracker_type == "minimize":
            period = f"Each {self.record_frequency} period.. "
            action_min = f"I {self.metric_action} a maximum {metric_min} {self.metric_unit}. "
            action_max = f"I take steps towards achieving {metric_max} {self.metric_unit}. "
            tsentence += " ".join([period, action_min, action_max])

        return tsentence

    def get_tquestion(self):
        return  self.get_tsentence() + " How did you get on?"

    def get_milestone_sentence(self):
        period_words = {"daily": "days", "weekly": "weeks", "monthly": "months", "yearly": "years", "custom":"custom"}
        sentence = ""
        if self.complete_allowed:
            value = str(self.complete_value)
            criteria = str(self.complete_criteria)
            period = period_words[self.record_frequency]
            sentence += " ".join([value, criteria, period])
        else:
            sentence += "No milestone set"
        return sentence

    def get_heatmap_dataframe(self):
        today = datetime.today()

        qs = StepTrackerLog.objects.filter(on_tracker=self)
        if qs:


            #df, vmin, vmax = self.daily_heatmap(self)
            df = pd.DataFrame.from_records(StepTrackerLog.objects.filter(on_tracker=self).values("create_date", "create_time","count_value", "submit_type"))
            df['date_time'] = pd.to_datetime(df['create_date'].astype(str) + df['create_time'].astype(str), format = '%Y-%m-%d%H:%M:%S')
            df = df[['date_time', 'submit_type', 'count_value']]
            df = df.sort_values('date_time', ascending=True)
            if self.metric_tracker_type == 'boolean':
                if self.minimum_show_allowed:
                    vmin=0.0
                    vmax=2.0
                else:
                    vmin=0.0
                    vmax=1.0
                df.loc[df['submit_type'] =='fail_or_no_submit', 'count_value'] = vmin
                df.loc[df['submit_type'] =='boolean_success', 'count_value'] = vmax
            else:
                if self.minimum_show_allowed:
                    if self.metric_tracker_type == 'maximize':
                        vmin = self.metric_min - 1
                        vmax = self.metric_max
                    else:
                        vmin = self.metric_min + 1
                        vmax = self.metric_max
                else:
                    vmin=self.metric_min
                    vmax=self.metric_max
            df.loc[df['submit_type'] =='min_showup', 'count_value'] = vmin
            for i, r in df.iterrows():
                print(r['date_time'], r['submit_type'], r['count_value'])
                print(type(r['date_time']))
            df = df[['date_time', 'count_value']]
            df = df.set_index('date_time')
        else:
            df = pd.DataFrame()
            vmin = 0
            vmax = 0
        df['count_value'] = df['count_value'].astype('float64')
        return (df, (vmin, vmax))

    def get_status_dict(self):
        status_dict = {
            "tracker": self,
            "logs_required": None,
            "total_logs": None,
            "period_log_start": None,
            "period_log_end": None,
            "boolean_status": None,
            "count_status": None,
            "count_quantity": None,
            "count_total": None,
            "tracker_graph": None,
        }

class StepTrackerLog(models.Model):
    TRACKER_LOG_TYPE = (
                        ("min_showup","minimum show"),
                        ("count_value","count submit"),
                        ("boolean_success", "boolean complete"),
                        ("fail_or_no_submit", "did not complete"),
                        )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    on_tracker = models.ForeignKey(StepTracker, on_delete=models.CASCADE, related_name="tracker_logs")
    create_date = models.DateField(default=now)
    create_time = models.TimeField(default=now)
    submit_type = models.CharField(max_length=100, choices=TRACKER_LOG_TYPE)
    count_value = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"TrackerLog_{self.id}"


class StepTrackerCustomFrequency(models.Model):
    on_tracker = models.ForeignKey(StepTracker, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, choices=CUSTOM_LOG_CODES)
