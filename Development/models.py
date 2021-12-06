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
from .utils import get_next_sunday, reverse_values #generate_heatmap_from_df
from .char_choices import *
import pandas as pd
import numpy as np
import io, urllib, base64
# import matplotlib.pyplot as plt
from .char_choices import *
from sklearn.preprocessing import MinMaxScaler


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


    def get_calmap_data(self):
        print("Here--------------------------->")
        print(self.id)
        # 1. get a list of date ranges from when the tracking begins until the current date
        historical_date_ranges = self.get_period_history()
        print(f"length of historical_date_ranges {len(historical_date_ranges)}")
        data_dict = {
                    "cal_date": [],
                    "period_start": [],
                    "period_end":[],
                    "calmap_value":[],
                    "count_value": [],
                    "adjusted_count_value": [],
                    }

        # 2. for each date range filter log results
        for (start_date, end_date) in historical_date_ranges:
            print(start_date.time())
            period_results = StepTrackerLog.objects.filter(on_tracker=self, create_datetime__range=[start_date, end_date])
            print(f"from {start_date} to {end_date}--->len results {len(period_results)}")
            for i in period_results:
                print(f"{i.id}----> length {len(period_results)}")
            # Assign the result to the count value
            if period_results:
                result_values = list(period_results.values_list('submit_type', flat=True))


                if "min_showup" in result_values:
                    calmap_value = 249
                    count_value = "You showed up!!"

                elif "fail_or_no_submit" in result_values:
                    calmap_value = 0
                    count_value = "Uncompleted"

                elif "boolean_success" in result_values:
                    calmap_value = 1000
                    count_value = "Completed"
                else:
                    calmap_value = np.nan
                    count_value = sum(list(period_results.values_list('count_value', flat=True)))
                    adjusted_count_value = np.nan

                    if self.metric_tracker_type == "minimize":
                        if count_value <= self.metric_max:
                            adjusted_count_value = self.metric_max
                        else:
                            adjusted_count_value = count_value
                        if count_value >= self.metric_min:
                            calmap_value = 250

                    elif self.metric_tracker_type == "maximize":
                        if count_value >= self.metric_max:
                            adjusted_count_value = self.metric_max
                        else:
                            adjusted_count_value = count_value
                        if count_value <= self.metric_min:
                            calmap_value = 250
                    else:
                        print("THE PROBLEM LIES HERE 181 ")
            else:
                calmap_value = 0
                count_value = "Uncompleted"
                adjusted_count_value = np.nan

        # 3. set each date in the date range to the log results

            cal_date = start_date.date()
            while cal_date < end_date.date():
                data_dict['cal_date'].append(cal_date)                                  # The date that will used on the calender
                data_dict['period_start'].append(start_date)                            # The date and time the logs period started
                data_dict['period_end'].append(end_date)                                # The date and time the logs period ended
                data_dict['count_value'].append(count_value)                            # The actual total of the logs for the period
                data_dict['calmap_value'].append(calmap_value)                          # The value the calendar heatmap will run off
                data_dict['adjusted_count_value'].append(adjusted_count_value)          # The interim value to be scaled to the heatmap range once all values have been found
                cal_date += relativedelta(days=1)

        # 4. create a dataframe and scale the adjusted count_value between 500 & 1000
        df = pd.DataFrame(data_dict)

        # Find all the places where a finalised calmap value has not been assigned
        nan_index = df['calmap_value'].isna()

        # Create a scaler to change those figuers into the range of 500-1000
        scaler = MinMaxScaler(feature_range=(500,1000))


        try:
            df.loc[nan_index, ['calmap_value']] = scaler.fit_transform(df.loc[nan_index, ['adjusted_count_value']])
            df['calmap_value'] = df['calmap_value'].round(4)
        except ValueError:
            print("no possible")


        # reverse count values for minimize
        if self.metric_tracker_type == "minimize":
            df['calmap_value'] = df['calmap_value'].apply(reverse_values)


        df = df.drop('adjusted_count_value', axis=1)
        df['cal_date'] = pd.to_datetime(df['cal_date'])

        return df



    def get_soonest_frequency_code(self):
        now = self.on_behaviour.on_aim.author.profile.today_to_user_time()
        soonest_date = None
        best_code = None
        code_duration = None
        all_custom_freq_code = list(StepTrackerCustomFrequency.objects.filter(on_tracker=self))
        for freq_code in all_custom_freq_code:
            var_date = now
            if freq_code.code in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                while var_date.strftime('%A') != freq_code.code:
                    var_date += relativedelta(days=1)
                if soonest_date:
                    if var_date < soonest_date:
                        soonest_date = var_date
                        best_code = freq_code.code
                        code_duration = 'daily'
                else:
                    soonest_date = var_date
                    best_code = freq_code.code
                    code_duration = 'daily'

            elif freq_code.code in range(1,32):
                while var.strftime('%-d') != freq_code.code:
                    var_date += relativedelta(days=1)
                if soonest_date:
                    if var_date < soonest_date:
                        soonest_date = var_date
                        best_code = freq_code.code
                        code_duration = 'monthly'
                else:
                    soonest_date = var_date
                    best_code = freq_code.code
                    code_duration = 'monthly'

            elif freq_code.code in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]:
                while var_date.strftime('%B') != freq_code.code:
                    var_date += relativedelta(months=1)
                if soonest_date:
                    if var_date < soonest_date:
                        soonest_date = var_date
                        best_code = freq_code.code
                        code_duration = 'monthly'
                else:
                    soonest_date = var_date
                    best_code = freq_code.code
                    code_duration = 'monthly'
            else:
                print("errors finding freq_code")
        return (soonest_date, freq_code.code, code_duration)

    def get_next_period(self):
        """
        Gets the next submission period for a tracker. Based on the users profile settings and the tracker length.
        Returns a start and end date for that period.
        Example:
        If period length is a day that starts on the 1st of January 2021 and the user profile reset time is 6am then the submission
        period is 01/01/21 @ 6am -> 02/01/21 @ 5:59am.
        If its a week period 01[user reset day of week]/01/21 @ 6am -> 08[user reset day of week + 7]/01/21 @5:59am.

        """
        period_length_conversion = {}
        member_profile = self.on_behaviour.on_aim.author.profile
        now = datetime.today()
        if self.record_frequency =="daily":
            user_time = member_profile.today_to_user_time()
            if now > user_time:
                start_date = user_time
                end_date = user_time + timedelta(hours=23, minutes=59, seconds=59)
            else:
                start_date = user_time - timedelta(hours=24)
                end_date =  user_time - timedelta(seconds=1)

        elif self.record_frequency =="weekly":
            user_time = member_profile.today_to_user_weekday_time()
            if now > user_time:
                start_date = user_time
                end_date = user_time + timedelta(days=6, hours=23, minutes=59, seconds=59)
            else:
                start_date = user_time - relativedelta(days=7)
                end_date =  user_time - timedelta(seconds=1)
        elif self.record_frequency =="monthly":
            user_time = member_profile.today_to_user_monthdate_time()
            if now > user_time:
                start_date = user_time
                end_date = user_time + relativedelta(months=1) - timedelta(seconds=1)
            else:
                start_date = user_time - relativedelta(months=1)
                end_date =  user_time - timedelta(seconds=1)
        else:
            user_time, freq_code, log_length = self.get_soonest_frequency_code()
            if log_length == 'daily':
                 if now > user_time:
                     start_date = user_time
                     end_date = user_time + relativedelta(months=1) - timedelta(seconds=1)
                 else:
                     start_date = user_time - relativedelta(months=1)
                     end_date =  user_time - timedelta(seconds=1)
            if log_length == "weekly":
                if now > user_time:
                    start_date = user_time
                    end_date = user_time + timedelta(days=6, hours=23, minutes=59, seconds=59)
                else:
                    start_date = user_time - relativedelta(days=7)
                    end_date =  user_time - timedelta(seconds=1)

            if log_length == 'monthly':
                 if now > user_time:
                     start_date = user_time
                     end_date = user_time + relativedelta(months=1) - timedelta(seconds=1)
                 else:
                     start_date = user_time - relativedelta(months=1)
                     end_date =  user_time - timedelta(seconds=1)

        return (start_date, end_date)

    def get_period_history(self):
        historical_date_ranges = []
        start_date, end_date = self.get_first_period()
        finish_date = get_next_sunday()
        if self.record_frequency == "daily":
            while start_date <= finish_date:
                historical_date_ranges.append((start_date, end_date))
                start_date += relativedelta(days=1)
                end_date += relativedelta(days=1)
        elif self.record_frequency == "weekly":
            while start_date <= finish_date:
                historical_date_ranges.append((start_date, end_date))
                start_date += relativedelta(days=7)
                end_date += relativedelta(days=7)
        elif self.record_frequency == "monthly":
            while start_date <= finish_date:
                historical_date_ranges.append((start_date, end_date))
                start_date += relativedelta(months=1)
                end_date += relativedelta(months=1)
        elif self.record_frequency == "yearly":
            while start_date <= finish_date:
                historical_date_ranges.append((start_date, end_date))
                start_date += relativedelta(years=1)
                end_date += relativedelta(years=1)
        else:
            all_custom_freq_code = list(StepTrackerCustomFrequency.objects.filter(on_tracker=self))
            for freq_code in all_custom_freq_code:
                tmp_start_date = start_date
                tmp_end_date = end_date
                if freq_code.code in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                    while tmp_start_date <= finish_date:
                        if tmp_start_date.strftime("%A") == freq_code.code:
                            historical_date_ranges.append((tmp_start_date,tmp_end_date))
                        tmp_start_date += relativedelta(days=1)
                        tmp_end_date += relativedelta(days=1)
                elif freq_code.code in [str(i) for i in range(1,32)]:
                    while tmp_start_date <= finish_date:
                        if tmp_start_date.strftime("%-d") == freq_code.code:
                            historical_date_ranges.append((tmp_start_date,tmp_end_date))
                        tmp_start_date += relativedelta(days=1)
                        tmp_end_date += relativedelta(days=1)
                elif freq_code.code in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]:
                    while tmp_start_date <= finish_date:
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
                while start_date.strftime('%-d') != str(member_profile.month_reset_day):
                    start_date += relativedelta(days=1)

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
            current_period_logs = StepTrackerLog.objects.filter(on_tracker=self, create_datetime__range=[start_date, end_date])
            period_statuses = list(current_period_logs.values_list('submit_type', flat=True))
            if "min_showup" in period_statuses or "fail_or_no_submit" in period_statuses or "boolean_success" in period_statuses:
                status = "period_complete"
            else:
                status = "period_progressing"
                if self.metric_tracker_type != "boolean":
                    value_counts = list(current_period_logs.values_list('count_value', flat=True))
                    total_logs = len(value_counts)
                    total_value_count = sum([int(i) for i in value_counts if i != None])

        else:
            status = "period_not_begun"
        return (status, total_logs, total_value_count)

    def get_tracker_display_section(self, start_date, end_date):
        now = datetime.today()
        in_future = relativedelta(end_date, start_date).days
        if in_future  <= 0:
            return "displayToday"
        elif in_future <= 7:
            return "displayWeek"
        elif in_future <= 31:
            return "displayMonth"
        else:
            return "displayYear"

    def get_status_dict(self):
        self.get_calmap_data()
        start, end = self.get_next_period()
        display_section = self.get_tracker_display_section(start, end)
        status, total_logs, total_log_values = self.get_current_period_status()
        s,e = self.get_first_period()
        period_history = self.get_period_history()
        status_dict = {
            "tracker": self,
            "next_period_start": start,
            "next_period_end": end,
            "next_period_status": status,
            "next_period_log_counts": total_logs,
            "next_period_log_total_value": total_log_values,
            "all_periods_to_date":period_history,
            "display_section": display_section, #progressing #complete
        }
        return status_dict

class StepTrackerLog(models.Model):
    TRACKER_LOG_TYPE = (
                        ("min_showup","minimum show"),
                        ("count_value","count submit"),
                        ("boolean_success", "boolean complete"),
                        ("fail_or_no_submit", "did not complete"),
                        )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    on_tracker = models.ForeignKey(StepTracker, on_delete=models.CASCADE, related_name="tracker_logs")
    create_datetime = models.DateTimeField(default=now)
    # create_date = models.DateField(default=now)
    # create_time = models.TimeField(default=now)
    submit_type = models.CharField(max_length=100, choices=TRACKER_LOG_TYPE)
    count_value = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"TrackerLog_{self.id}"


class StepTrackerCustomFrequency(models.Model):
    on_tracker = models.ForeignKey(StepTracker, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, choices=CUSTOM_LOG_CODES)
