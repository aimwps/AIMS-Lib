from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator
from WebsiteTools.models import ContentCategory
from django.utils.timezone import now
from Members.models import MemberProfile
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
        historical_date_ranges = self.get_period_history()
        df = pd.DataFrame.from_records(StepTrackerLog.objects.filter(on_tracker=self).values("create_date", "create_time","count_value", "submit_type"))
        df['date_time'] = pd.to_datetime(df['create_date'].astype(str) + df['create_time'].astype(str), format = '%Y-%m-%d%H:%M:%S')
        df = df[['date_time', 'submit_type', 'count_value']]
        df = df.sort_values('date_time', ascending=True)
        heatmap_df = pd.DataFrame({"date_time":[], "heatmap_value":[]})
        if self.metric_tracker_type =="boolean":
            vmin=1.0
            vmax=3.0
        else:
            vmin=self.metric_max
            vmax=self.metric_max*3
            count_start = self.metric_max-self.metric_min
        if self.minimum_show_allowed:
            vmin += self.
            vmax += .0
        if self.record_log_length =="day":
            for date in historical_date_ranges:
                found_records = df[df['date_time']>=date[0] & df['date_time']<=date[1]]
                if len(found_records)==0:
                    heatmap_df.append({"date_time":date[0]+ relativedelata(hours=12),
                                        "heatmap_value":0})
                if len(found_records)==1:
                    if "submit_type"



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
            df = df[['date_time', 'count_value']]
            df = df.set_index('date_time')
        else:
            df = pd.DataFrame({"create_date":[],
                                "count_value": []})
            vmin = 0
            vmax = 0
        df['count_value'] = df['count_value'].astype('float64')
        return (df, (vmin, vmax))


##########
    #today = datetime.today()
        #
        # qs = StepTrackerLog.objects.filter(on_tracker=self)
        # if qs:
        #     df = pd.DataFrame.from_records(StepTrackerLog.objects.filter(on_tracker=self).values("create_date", "create_time","count_value", "submit_type"))
        #     df['date_time'] = pd.to_datetime(df['create_date'].astype(str) + df['create_time'].astype(str), format = '%Y-%m-%d%H:%M:%S')
        #     df = df[['date_time', 'submit_type', 'count_value']]
        #     df = df.sort_values('date_time', ascending=True)
        #     if self.metric_tracker_type == 'boolean':
        #         if self.minimum_show_allowed:
        #             vmin=0.0
        #             vmax=2.0
        #         else:
        #             vmin=0.0
        #             vmax=1.0
        #         df.loc[df['submit_type'] =='fail_or_no_submit', 'count_value'] = vmin
        #         df.loc[df['submit_type'] =='boolean_success', 'count_value'] = vmax
        #     else:
        #         if self.minimum_show_allowed:
        #             if self.metric_tracker_type == 'maximize':
        #                 vmin = self.metric_min - 1
        #                 vmax = self.metric_max
        #             else:
        #                 vmin = self.metric_min + 1
        #                 vmax = self.metric_max
        #         else:
        #             vmin=self.metric_min
        #             vmax=self.metric_max
        #     df.loc[df['submit_type'] =='min_showup', 'count_value'] = vmin
        #     df = df[['date_time', 'count_value']]
        #     df = df.set_index('date_time')
        # else:
        #     df = pd.DataFrame({"create_date":[],
        #                         "count_value": []})
        #     vmin = 0
        #     vmax = 0
        # df['count_value'] = df['count_value'].astype('float64')
        # return (df, (vmin, vmax))

    def get_heatmap(self):
        pass
    def get_next_period(self):
        member_profile = MemberProfile.objects.get(author=self.on_behaviour.on_aim.author.id)
        now = datetime.today()
        reset_user_time = datetime.combine(now, member_profile.day_reset_time)
        reset_user_date_time = reset_user_time + relativedelta(day=member_profile.month_reset_day)
        reset_user_year_date_time = reset_user_date_time + relativedelta(month=member_profile.year_reset_month)
        if self.record_log_length == "day":
            if self.record_frequency =="daily":
                if now > reset_user_time:
                    start_date = reset_user_time
                    end_date =  reset_user_time + timedelta(hours=23, minutes=59, seconds=59)
                else:
                    start_date = reset_user_time - timedelta(hours=24)
                    end_date =  reset_user_time - timedelta(seconds=1)
            else:
                all_custom_freq_code = list(StepTrackerCustomFrequency.objects.filter(on_tracker=self))
                soonest_date = None
                for freq_code in all_custom_freq_code:
                    temp_reset_user_time = reset_user_time
                    if freq_code.code in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                        while temp_reset_user_time.strftime('%A') != freq_code.code:
                            temp_reset_user_time += relativedelta(days=1)
                        if soonest_date:
                            if soonest_date > temp_reset_user_time:
                                soonest_date = temp_reset_user_time
                        else:
                            soonest_date = temp_reset_user_time
                    if freq_code.code in range(1,32):
                        while temp_reset_user_time.strftime('%d') != freq_code.code:
                            temp_reset_user_time += relativedelta(days=1)
                        if soonest_date:
                            if soonest_date > temp_reset_user_time:
                                soonest_date = temp_reset_user_time
                        else:
                            soonest_date = temp_reset_user_time
                if now > soonest_date:
                    start_date = soonest_date
                    end_date =  soonest_date+ timedelta(hours=23, minutes=59, seconds=59)
                else:
                    start_date = soonest_date - timedelta(hours=24)
                    end_date =  soonest_date - timedelta(seconds=1)

            return start_date, end_date

        elif self.record_log_length == "week":
            if self.record_frequency =="weekly":
                if reset_user_time.strftime('%A') == member_profile.week_reset_day:
                    if now > reset_user_time:
                        start_date = reset_user_time
                        end_date =  reset_user_time + timedelta(days=6, hours = 23, minutes=59, seconds=59)
                    else:
                        start_date = reset_user_time - timedelta(days=7)
                        end_date =  reset_user_time - timedelta(seconds=1)
                else:
                    while reset_user_time.strftime('%A') != member_profile.week_reset_day:
                        reset_user_time += timedelta(days=1)
                    end_date = reset_user_time - timedelta(seconds=1)
                    start_date = reset_user_time - timedelta(days=7)
            else:
                print("Custom weeks not avalabile yet")
                all_custom_freq_code = list(StepTrackerCustomFrequency.objects.filter(on_tracker=self))
            return start_date, end_date

        elif self.record_log_length == "month":
            if self.record_frequency == "monthly":
                if reset_user_date_time.strftime('%d') == str(member_profile.month_reset_day).zfill(2):
                    if now > reset_user_date_time:
                        start_date = reset_user_date_time
                        end_date =  reset_user_date_time + relativedelta(months=1) - timedelta(seconds=1)
                    else:
                        start_date = reset_user_date_time - relativedelta(months=1)
                        end_date =  reset_user_date_time - timedelta(seconds=1)
                elif reset_user_date_time.strftime('%d') > str(member_profile.month_reset_day).zfill(2):
                    start_date = reset_user_date_time - relativedelta(months=1)
                    end_date =  reset_user_date_time - timedelta(seconds=1)
                else:
                    start_date = reset_user_date_time
                    end_date =  reset_user_date_time + relativedelta(months=1) - timedelta(seconds=1)
            else:
                all_custom_freq_code = list(StepTrackerCustomFrequency.objects.filter(on_tracker=self))
                soonest_date = None
                for freq_code in all_custom_freq_code:
                    if freq_code.code in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]:
                        temp_reset_user_time = reset_user_date_time
                        while temp_reset_user_time.strftime('%B') != freq_code.code:
                            temp_reset_user_time += relativedelta(months=1)

                        if soonest_date:
                            if soonest_date > temp_reset_user_time:
                                soonest_date = temp_reset_user_time
                        else:
                            soonest_date = temp_reset_user_time
                start_date = soonest_date
                end_date =  soonest_date + relativedelta(months=1) - timedelta(seconds=1)
            return start_date, end_date
        elif self.record_log_length == "year":
            if reset_user_year_date_time.strftime('%m') == str(member_profile.year_reset_month).zfill(2):
                if now > reset_user_year_date_time:
                    start_date = reset_user_year_date_time
                    end_date  = reset_user_year_date_time + relativedelta(years=1) - timedelta(seconds=1)
                else:
                    start_date = reset_user_date_time - relativedelta(years=1)
                    end_date =  reset_user_date_time - timedelta(seconds=1)
            elif reset_user_year_date_time.strftime('%m') > str(member_profile.year_reset_month).zfill(2):
                start_date = reset_user_date_time - relativedelta(years=1)
                end_date =  reset_user_date_time - timedelta(seconds=1)
            else:
                start_date = reset_user_date_time
                end_date =  reset_user_date_time + relativedelta(years=1) - timedelta(seconds=1)
            return start_date, end_date
        else:
            print("big errors 351")

    def get_period_history(self):
        historical_date_ranges = []
        start_date, end_date = self.get_first_period()
        if self.record_frequency == "daily":
            while start_date <= datetime.now():
                historical_date_ranges.append((start_date, end_date))
                start_date += relativedelta(days=1)
                end_date += relativedelta(days=1)
        elif self.record_frequency == "weekly":
            while start_date <= datetime.now():
                historical_date_ranges.append((start_date, end_date))
                start_date += relativedelta(days=7)
                end_date += relativedelta(days=7)
        elif self.record_frequency == "monthly":
            while start_date <= datetime.now():
                historical_date_ranges.append((start_date, end_date))
                start_date += relativedelta(months=1)
                end_date += relativedelta(months=1)
        elif self.record_frequency == "yearly":
            while start_date <= datetime.now():
                historical_date_ranges.append((start_date, end_date))
                start_date += relativedelta(years=1)
                end_date += relativedelta(years=1)
        else:
            all_custom_freq_code = list(StepTrackerCustomFrequency.objects.filter(on_tracker=self))
            for freq_code in all_custom_freq_code:
                tmp_start_date = start_date
                tmp_end_date = end_date
                if freq_code.code in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                    while tmp_start_date <= datetime.now():
                        if tmp_start_date.strftime("%A") == freq_code.code:
                            historical_date_ranges.append((tmp_start_date,tmp_end_date))
                        tmp_start_date += relativedelta(days=1)
                        tmp_end_date += relativedelta(days=1)
                elif freq_code.code in [str(i) for i in range(1,32)]:
                    while tmp_start_date <= datetime.now():
                        if tmp_start_date.strftime("%-d") == freq_code.code:
                            historical_date_ranges.append((tmp_start_date,tmp_end_date))
                        tmp_start_date += relativedelta(days=1)
                        tmp_end_date += relativedelta(days=1)
                elif freq_code.code in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]:
                    while tmp_start_date <= datetime.now():
                        if tmp_start_date.strftime("%B") == freq_code.code:
                            historical_date_ranges.append((tmp_start_date,tmp_end_date))
                        tmp_start_date += relativedelta(months=1)
                        tmp_end_date += relativedelta(months=1)
                else:
                    print(f"unrecognised freq_code: {freq_code.code}")
        return historical_date_ranges

    def get_first_period(self):
        member_profile = MemberProfile.objects.get(author=self.on_behaviour.on_aim.author.id)
        now = datetime.today()
        if self.record_log_length == "day":
            if self.record_frequency =="daily":
                start_date = datetime.combine(self.record_start_date, member_profile.day_reset_time)
                end_date = start_date + relativedelta(days=1) - timedelta(seconds=1)
            else:
                all_custom_freq_code = list(StepTrackerCustomFrequency.objects.filter(on_tracker=self))
                soonest_date = None
                for freq_code in all_custom_freq_code:
                    temp_reset_user_time = self.record_start_date
                    if freq_code.code in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                        while temp_reset_user_time.strftime('%A') != freq_code.code:
                            temp_reset_user_time += relativedelta(days=1)
                        if soonest_date:
                            if soonest_date > temp_reset_user_time:
                                soonest_date = temp_reset_user_time
                        else:
                            soonest_date = temp_reset_user_time
                    if freq_code.code in range(1,32):
                        while temp_reset_user_time.strftime('%d') != freq_code.code:
                            temp_reset_user_time += relativedelta(days=1)
                        if soonest_date:
                            if soonest_date > temp_reset_user_time:
                                soonest_date = temp_reset_user_time
                        else:
                            soonest_date = temp_reset_user_time
                start_date = datetime.combine(soonest_date, member_profile.day_reset_time)
                end_date = start_date + relativedelta(days=1) - timedelta(seconds=1)
        elif self.record_log_length == "week":
            if self.record_frequency == "weekly":
                start_date = datetime.combine(self.record_start_date, member_profile.day_reset_time)

                while start_date.strftime('%A') != member_profile.week_reset_day:
                    start_date -= relativedelta(days=1)
                end_date = start_date + relativedelta(weeks=1) - timedelta(seconds=1)
            else:
                print("error 2 custom weekly going here")
        elif self.record_log_length =="month":
            if self.record_frequency =="monthly":
                start_date = datetime.combine(self.record_start_date, member_profile.day_reset_time)
                while start_date.strftime('%d') != str(member_profile.month_reset_day).zfill(2):
                    start_date += relativedelata(months=1)
                end_date = start_date + relativedelta(months=1) - timedelta(seconds=1)
            else:
                all_custom_freq_code = list(StepTrackerCustomFrequency.objects.filter(on_tracker=self))
                soonest_date = None
                for freq_code in all_custom_freq_code:
                    temp_reset_user_time = self.record_start_date
                    if freq_code.code in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]:
                        while temp_reset_user_time.strftime('%B') != freq_code.code:
                            temp_reset_user_time += relativedelta(months=1)
                        if soonest_date:
                            if soonest_date > temp_reset_user_time:
                                soonest_date = temp_reset_user_time
                        else:
                            soonest_date = temp_reset_user_time

                start_date = datetime.combine(soonest_date, member_profile.day_reset_time)
                end_date = start_date + relativedelta(months=1) - timedelta(seconds=1)
        else:
            reset_user_time = datetime.combine(self.record_start_date, member_profile.day_reset_time)
            reset_user_date_time = reset_user_time + relativedelta(day=member_profile.month_reset_day)
            reset_user_year_date_time = reset_user_date_time + relativedelta(month=member_profile.year_reset_month)
            if reset_user_year_date_time > now:
                start_date = reset_user_year_date_time - relativedelta(years=1)
                end_date = reset_user_year_date_time - timedelta(seconds=1)
            else:
                start_date = reset_user_year_date_time
                end_date = reset_user_year_date_time + relativedelta(years=1) - timedelta(seconds=1)
        return start_date, end_date


    def get_current_period_status(self):
        status= None
        total_logs = None
        total_value_count = None
        start_date, end_date = self.get_next_period()

        if start_date < datetime.now() < end_date:
            current_period_logs = StepTrackerLog.objects.filter(on_tracker=self, create_date__range=[start_date, end_date])
            period_statuses = list(current_period_logs.values_list('submit_type', flat=True))
            if "min_showup" in period_statuses or "fail_or_no_submit" in period_statuses or "boolean_success" in period_statuses:
                status = "period_complete"
            else:
                status = "period_progressing"
                if self.metric_tracker_type != "boolean":
                    value_counts = list(current_period_logs.values_list('count_value', flat=True))
                    total_logs = len(value_counts)
                    total_value_counts = sum([int(i) for i in value_counts if i != None])
        else:
            status = "period_not_begun"
        return (status, total_logs, total_value_count)

    def get_status_dict(self):
        start, end = self.get_next_period()
        status, total_logs, total_log_values = self.get_current_period_status()
        s,e = self.get_first_period()
        print(f"{self}|| Start: {s} End: {e}")
        period_history = self.get_period_history()
        for p in period_history:
            print(p)
        status_dict = {
            "tracker": self,
            "next_period_start": start,
            "next_period_end": end,
            "next_period_status": status,
            "next_period_log_counts": total_logs,
            "next_period_log_total_value": total_log_values,
            "all_periods_to_date":period_history, #progressing #complete
            "current_period_count": None,
            "heatmap_dataframe": None,
            "logs_required": None,
            "total_logs": None,
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
