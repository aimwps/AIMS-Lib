from django.shortcuts import render, get_object_or_404
from .models import Aim, Lever, TrackerMinAim, DevelopmentCategory, MinAimRecords
from Members.models import MemberProfile
from .forms import AimNewForm, LeverNewForm, TrackerMinAimNewForm, MinAimRecordsForm
from django.views.generic import TemplateView, CreateView, View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from datetime import datetime, timedelta

class LogTracker(CreateView):
    model = MinAimRecords
    form_class = MinAimRecordsForm
    template_name = "min_aim_new_log.html"
    def form_valid(self, form):
        form.instance.tracker =TrackerMinAim.objects.get(id=self.kwargs['tracker_id'])
        form.instance.lever_performed = True
        #self.in_category = get_object_or_404(DevelopmentCategory, id=SkillArea.objects.filter(skill_area_name=self.kwargs['dev_area_name'])[0].id)
        return super().form_valid(form)


class AssignTrackerView(View):
    template_name = "tracker_select.html"

    def get(self, request, lever_id):
        context = {"min_aim_form": TrackerMinAimNewForm(),
                    "on_lever": Lever.objects.get(id=lever_id)}

        return render(request, self.template_name, context)

    def form_valid(self, form):
        form.instance.on_lever = Lever.objects.get(id=self.kwargs['lever_id'])
        return super().form_valid(form)


    def post(self, request, lever_id):

        if "min_aim_tracker_submit" in request.POST:
            min_aim_form = TrackerMinAimNewForm(request.POST)
            if min_aim_form.is_valid():

                new_tracker = TrackerMinAim(
                            lever = Lever.objects.get(id=lever_id),
                            metric_type = min_aim_form.cleaned_data['metric_type'],
                            metric_min = min_aim_form.cleaned_data['metric_min'],
                            metric_aim = min_aim_form.cleaned_data['metric_aim'],
                            metric_description = min_aim_form.cleaned_data['metric_description'],
                            frequency = min_aim_form.cleaned_data['frequency'],
                            start_date = min_aim_form.cleaned_data['start_date'],
                            end_date = min_aim_form.cleaned_data['end_date'],
                            complete_criteria = min_aim_form.cleaned_data['complete_criteria'],
                            complete_value = min_aim_form.cleaned_data['complete_value'])


                new_tracker.save()

                return HttpResponseRedirect('/aims_dash/')
            else:
                context = {"min_aim_form": TrackerMinAimNewForm(request.POST),
                            "on_lever": Lever.objects.get(id=lever_id)}

                return render(request, self.template_name, context)





# Create your views here.
class LeverNew(CreateView):
    model = Lever
    form_class = LeverNewForm
    template_name = "lever_new.html"

    def form_valid(self, form):
        #self.in_category = get_object_or_404(DevelopmentCategory, id=SkillArea.objects.filter(skill_area_name=self.kwargs['dev_area_name'])[0].id)
        form.instance.on_aim = Aim.objects.get(id=self.kwargs['aim_id'])
        # For getting and resetting the correct order
        all_aim_levers = Lever.objects.filter(on_aim=self.kwargs['aim_id']).order_by('in_order')

        for i, lever in  enumerate(all_aim_levers):
            lever.in_order =  i
            lever.save()
        form.instance.in_order = len(all_aim_levers)
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aim_for_lever'] = Aim.objects.get(id=self.kwargs['aim_id'])
        return context




class AimNew(CreateView):
    model = Aim
    form_class = AimNewForm
    template_name = "aim_new.html"
    def form_valid(self, form):
        #self.in_category = get_object_or_404(DevelopmentCategory, id=SkillArea.objects.filter(skill_area_name=self.kwargs['dev_area_name'])[0].id)
        form.instance.user = self.request.user
        return super().form_valid(form)


class AimView(TemplateView):
    template_name = "aims.html"
    #form_class = ForumTopicNewComment
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aims = []
        for aim in Aim.objects.filter(user=self.request.user.id):
            aims.append(aim)
        context['aims_list'] = aims
        return context


class AimsDash(TemplateView):
    template_name = "aims_dash.html"
    #form_class = ForumTopicNewComment
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aims_by_cat = []

    # For gethering info on trackers
        uncomplete_daily = []
        uncomplete_weekly = []
        uncomplete_monthly = []
        uncomplete_yearly = []
        #TrackerMinAim.objects.filter(lever__on_aim__user__id=self.request.user.id, frequency="daily")
         #outstanding_daily = self.get_daily_outstanding(trackers_by_daily)
        trackers_by_weekly = TrackerMinAim.objects.filter(lever__on_aim__user__id=self.request.user.id, frequency="weekly")
        trackers_by_monthly = TrackerMinAim.objects.filter(lever__on_aim__user__id=self.request.user.id, frequency="monthly")
        trackers_by_yearly = TrackerMinAim.objects.filter(lever__on_aim__user__id=self.request.user.id, frequency="yearly")

    # For building cascading dictionaries for displaying aims
        # Loop through every category
        for cat in DevelopmentCategory.objects.all():
            all_cat_aim_data = {}

            ## Get the category trail e.g. mindset -> meditation
            full_cat_path = get_category_path(cat)

            # for eveter category we collect the page users cateogory aims
            cat_aims = Aim.objects.filter(user=self.request.user.id, category=cat.id)

            # Loop thorugh all the aims in that category
            for aim in cat_aims:
                aim_levers = {}
                all_aim_levers = Lever.objects.filter(on_aim = aim.id).order_by("in_order")

            # For each aim in a category, find the corresponding Levers
                # get all the trackers for that lever.
                for lever in all_aim_levers:
                    lever_trackers = {}
                    trackers = lever.get_trackers()

            # Check all trackers for a lever. While looping through trackers check if
            # they have the correct amount of logs for the current period.
            # If they do not, add the tracker to the relevant time slot list. ('daily, weekly etc')
                    for tracker in trackers:
                        tracker_complete, freq_bracket = self.check_tracker_status(tracker)
                        if not tracker_complete:
                            eval(f"uncomplete_{freq_bracket}").append(tracker)
                        if isinstance(tracker, TrackerMinAim):
                            if "TrackerMinAim" in lever_trackers.keys():
                                lever_trackers["TrackerMinAim"].append(tracker)
                            else:
                                lever_trackers["TrackerMinAim"] = [tracker]

            # Build the context dictionary
                    aim_levers[lever] = lever_trackers
                all_cat_aim_data[aim] = aim_levers
            aims_by_cat.append((full_cat_path, all_cat_aim_data))
        context['aims_by_cat'] = sorted(aims_by_cat)
        context['uncomplete_daily'] = uncomplete_daily
        context['uncomplete_weekly'] = uncomplete_weekly
        context['uncomplete_monthly'] = uncomplete_monthly
        context['uncomplete_yearly'] = uncomplete_yearly

        print(uncomplete_daily)
        print(uncomplete_weekly)
        print(uncomplete_monthly)
        print(uncomplete_yearly)
        return context





    def check_tracker_status(self, tracker):
        print(tracker)
        print(tracker.frequency)
        member_profile = MemberProfile.objects.get(user_profile=self.request.user.id)
        tracker_info  = {'tracker':tracker,}

        ## Check the type of tracker
        if isinstance(tracker, TrackerMinAim):

            # Get the logs for that type
            tracker_logs = MinAimRecords.objects.filter(tracker=tracker.id).order_by('record_date', 'record_time')
            now = datetime.today()
            reset_user_time = datetime.combine(now, member_profile.day_reset_time)
            # See the frequency a
            if tracker.frequency == "daily":
                # now = datetime.today()
                # reset_user_time = datetime.combine(now, member_profile.day_reset_time)
                if now > reset_user_time:
                    start_date = reset_user_time
                    end_date =  reset_user_time + timedelta(hours=23, minutes=59, seconds=59)
                else:
                    start_date = reset_user_time - time_delta(hours=24)
                    end_date =  reset_user_time - time_delta(seconds=1)

                # current_daily_period_logs = MinAimRecords.objects.filter(tracker=tracker.id,record_date__range=[start_date, end_date])
                # if current_daily_period_logs:
                #     if len(current_daily_period_logs) == tracker.frequency_quantity:
                #         return (True,'daily')
                # else:
                #     return ( False, 'daily')
            if tracker.frequency == "weekly":
                # now = datetime.today()
                # reset_user_time = datetime.combine(now, member_profile.day_reset_time)
                if reset_user_time.strftime('%A') == member_profile.week_reset_day:
                    if now > reset_user_time:
                        start_date = reset_user_time
                        end_date =  reset_user_time + timedelta(days=6, hours = 23, minutes=59, seconds=59)
                    else:
                        start_date = reset_user_time - time_delta(days=7)
                        end_date =  reset_user_time - time_delta(seconds=1)
                else:
                    while reset_user_time.strftime('%A') != member_profile.week_reset_day:
                        reset_user_time += timedelta(days=1)
                    end_date = reset_user_time - timedelta(seconds=1)
                    start_date = reset_user_time - timedelta(days=7)
            if tracker.frequency == "monthly":
                return (True, 'monthly')
            if tracker.frequency == "yearly":
                return (True, 'yearly')


            current_daily_period_logs = MinAimRecords.objects.filter(tracker=tracker.id,record_date__range=[start_date, end_date])
            if current_daily_period_logs:
                if len(current_daily_period_logs) == tracker.frequency_quantity:
                    return (True, tracker.frequency)
                else:
                    return (False, tracker.frequency)
            else:
                return (False, tracker.frequency)




    def create_range_time(self, start_date, end_date, time):
        today_with_member_time = start_date.replace(hour=time.hour, minute=time.minute, second=0, microsecond=0)
        if today_with_member_time > datetime.today():
            current_period_start = today_with_member_time - timedelta(days=1)
            current_period_end = today_with_member_time - timedelta(seconds=1)
            return (current_period_start, current_period_end)
        else:
            current_period_start = today_with_member_time
            current_period_end = today_with_member_time + timedelta(days=1) -timedelta(seconds=1)
            #current_period_end = current_period_end -timedelta(seconds=1)
            return (current_period_start, current_period_end)


### for a tracker

def get_category_path(cat, current_path=""):
    if cat.parent_category:
        new_path = " > "
        new_path += str(cat.title)
        new_path += current_path
        return get_category_path(cat.parent_category, current_path=new_path)

    else:
        new_path = str(cat.title)
        new_path += current_path
        return new_path
