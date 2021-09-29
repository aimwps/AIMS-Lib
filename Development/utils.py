def check_tracker_status(self, tracker):
        member_profile = MemberProfile.objects.get(user_profile=self.request.user.id)
        tracker_info  = {'tracker':tracker,}
        now = datetime.today()

        reset_user_time = datetime.combine(now, member_profile.day_reset_time)

        #reset_this_month = min(calendar.monthrange(now.year, now.month)[1], member_profile.month_reset_day)
        reset_user_date_time = reset_user_time + relativedelta(day=member_profile.month_reset_day)

        reset_user_year_date_time = reset_user_date_time + relativedelta(month=member_profile.year_reset_month)

        ### Set the start and end date range for tracker filter based on the frequency of the tracker
        if tracker.frequency == "daily":
            if now > reset_user_time:
                start_date = reset_user_time
                end_date =  reset_user_time + timedelta(hours=23, minutes=59, seconds=59)
            else:
                start_date = reset_user_time - timedelta(hours=24)
                end_date =  reset_user_time - timedelta(seconds=1)
        if tracker.frequency == "weekly":
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
        if tracker.frequency == "monthly":
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

        if tracker.frequency == "yearly":
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

        ## Check the type of tracker and filter the appropriate logs the logs for the tracker.
        #if isinstance(tracker, TrackerMinAim):
        current_period_logs = eval(f"{tracker.get_tclass()}Records").objects.filter(tracker=tracker.id,record_date__range=[start_date, end_date])
        if current_period_logs:
            if len(current_period_logs) >= tracker.frequency_quantity:
                return (True, tracker.frequency, start_date, end_date)
            else:
                return (False, tracker.frequency, start_date, end_date)
        else:
            return (False, tracker.frequency, start_date, end_date)


def prettify_boolean_log_dict(dict):
    dict_status_pretty = {"boolean_showup": "You showed up today",
                        "boolean_success": "Great success"}
    status = dict_status_pretty[dict['boolean_status']]
    return (dict["period_log_start"], dict['period_log_end'], status)

def prettify_count_log_dict(dict):
    dict_status_pretty = {}
    status = dict_status_pretty[dict['boolean_status']]
    return (dict["period_log_start"], dict['period_log_end'], status)

    if dict['tracker'].metric_tracker_type == "boolean":
        status = dict_status_pretty[dict['boolean_status']]
    else:
        status = dict_status_pretty[dict['count_status']]

    return (dict["period_log_start"], dict['period_log_end'], status, dict[])
            # "tracker": tracker,
            # "logs_required": None,
            # "total_logs": total_logs,
            # "period_log_start": start_date,
            # "period_log_end": end_date,
            # "boolean_status": None,
            # "count_status": None,
            # "count_quantity": None,
            # "count_total": None,
            # }
