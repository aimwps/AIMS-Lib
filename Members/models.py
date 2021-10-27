from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from ckeditor.fields import RichTextField
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
DAY_CHOICES = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
DAY_CHOICES = ((d,d) for d in DAY_CHOICES)
# Create your models here.
class MemberProfile(models.Model):
    author = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name="profile")
    power_quote = models.TextField(max_length=255, null=True, blank=True)
    profile_picture =  models.ImageField(null=True, blank=True, upload_to="path to images") ### STILL NEED TO SET IMAGE PATHS
    biography = RichTextField(config_name="article_editor", blank=True, null=True)
    personal_website = models.CharField(max_length=255, null=True, blank=True)
    linked_in = models.CharField(max_length=255, null=True, blank=True)
    day_reset_time = models.TimeField(default=datetime.time(datetime(1800, 12, 25, 5, 0,0,0)))
    week_reset_day = models.CharField(max_length=100, choices=DAY_CHOICES, default="Monday")
    month_reset_day = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1), MaxValueValidator(31)])
    year_reset_month = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1), MaxValueValidator(12)])
    create_date = models.DateField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)
    modify_date = models.DateField(auto_now=True,auto_now_add=False)
    modify_time = models.TimeField(auto_now=True,auto_now_add=False)

    def __str__(self):
        return str(self.user_profile)
    def today_to_user_time(self):
        now = datetime.today()
        return datetime.combine(now, self.day_reset_time)

    def today_to_user_weekday_time(self):
        res = self.today_to_user_time()
        while res.strftime('%A') != self.week_reset_day:
            res += relativedelta(days=1)
        return res

    def today_to_user_monthdate_time(self):
        res = self.today_to_user_time()
        while res.strftime('%-d') != str(self.month_reset_day):
            res += relativedelta(days=1)
        return res

    # def next_user_adjusted_week_period(self):
    #     pass
    # def next_user_adjusted_month_period(self):
    #     pass
    # def next_user_adjusted_year_period(self):
    #     pass



    # def get_reset_periods(self):
    #     now = datetime.today()
    #     reset_user_time = datetime.combine(now, self.day_reset_time)
    #     # The current_date e.g. 29/09/21 @ 14:30 set to users reset periods Time
    #                       # --> 29/09/21 @ 05:00
    #     reset_user_date_time = reset_user_time + relativedelta(day=self.month_reset_day)
    #     # The current_date e.g. 29/09/21 @ 14:30 set to users reset periods Time, Day
    #                       # --> 01/09/21 @ 05:00
    #
    #     reset_user_year_date_time = reset_user_date_time + relativedelta(month=self.year_reset_month)
    #     # The current date e.g. 29/09/21 @ 14:30 set to users reset periods Time, Day, Month
    #                       # --> 01/01/21 @ 05:00
    #     reset_periods = {"in_day_reset": reset_user_time,
    #                     "in_month_reset":reset_user_date_time,
    #                     "in_year_reset": reset_user_year_date_time}
    #     return reset_periods
