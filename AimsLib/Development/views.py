from django.shortcuts import render, get_object_or_404
from .models import Aim, Lever, TrackerMinAim, DevelopmentCategory, TrackerMinAimRecords, TrackerBoolean, TrackerBooleanRecords
from Members.models import MemberProfile
from .forms import AimNewForm, LeverNewForm, TrackerMinAimNewForm, TrackerMinAimRecordsForm, TrackerBooleanNewForm, TrackerBooleanRecordsForm
from django.views.generic import TemplateView, CreateView, View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from datetime import datetime, timedelta
import calendar
from dateutil.relativedelta import relativedelta
from collections import OrderedDict

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



class LogAnyTracker(View):
    template_name = "new_tracker_log.html"
    def get(self, request, tracker_type, tracker_id):
        context = {
                "tracker": eval(f"{tracker_type}").objects.get(id=self.kwargs['tracker_id']),
                "form": eval(f"{tracker_type}RecordsForm()")}
        return render(request, self.template_name, context)

    def form_valid(self, form):
        #print(f"checking form {form}")
        form.instance.tracker = eval(f"{tracker_type}Records").objects.get(id=self.kwargs['tracker_id'])
        return super().form_valid(form)

    def post(self, request, tracker_type, tracker_id):
        submit_form = eval(f"{tracker_type}RecordsForm(request.POST)")
        if submit_form.is_valid():
            if tracker_type == "TrackerMinAim":
                new_log = TrackerMinAimRecords(
                            tracker = TrackerMinAim.objects.get(id=tracker_id),
                            lever_performed = True,
                            metric_quantity = submit_form.cleaned_data['metric_quantity']
                            )
                new_log.save()
            if tracker_type == "TrackerBoolean":
                new_log = TrackerBooleanRecords(
                            tracker = TrackerBoolean.objects.get(id=tracker_id),
                            lever_performed = True,
                            metric_quantity = submit_form.cleaned_data['metric_quantity']
                            )
                print(f"metric quantity {submit_form.cleaned_data['metric_quantity']}")
                new_log.save()
            return HttpResponseRedirect('/aims_dash/')
        else:
            print("ERRRRRRRRRRRRRRRRRRRROOOOOOOOOOOOOOOOOORRR")
            return HttpResponseRedirect('/aims_dash/')




class AssignTrackerView(View):
    template_name = "tracker_select.html"

    def get(self, request, lever_id):
        context = {"min_aim_form": TrackerMinAimNewForm(),
                    "boolean_form": TrackerBooleanNewForm(),
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

        elif "boolean_submit" in request.POST:
            boolean_form = TrackerBooleanNewForm(request.POST)
            if boolean_form.is_valid():
                new_tracker = TrackerBoolean(
                            lever = Lever.objects.get(id=lever_id),
                            metric_description = boolean_form.cleaned_data['metric_description'],
                            frequency = boolean_form.cleaned_data['frequency'],
                            start_date = boolean_form.cleaned_data['start_date'],
                            end_date = boolean_form.cleaned_data['end_date'],
                            complete_criteria = boolean_form.cleaned_data['complete_criteria'],
                            complete_value = boolean_form.cleaned_data['complete_value'])
                new_tracker.save()
                return HttpResponseRedirect('/aims_dash/')
            else:
                print("form error")
        else:
            return HttpResponseRedirect('/aims_dash/')






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
        all_uncomplete_tracker_periods = ['uncomplete_daily','uncomplete_weekly', 'uncomplete_monthly', 'uncomplete_yearly']
        uncomplete_trackers = OrderedDict({
                                    'daily': None,
                                    'weekly': None,
                                    'monthly':  None,
                                    'yearly': None,})
        uncomplete_daily = []
        uncomplete_weekly = []
        uncomplete_monthly = []
        uncomplete_yearly = []

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
                        tracker_complete, freq_bracket, start_date, end_date = self.check_tracker_status(tracker)
                        if not tracker_complete:
                            if uncomplete_trackers[freq_bracket] != None:
                                uncomplete_trackers[freq_bracket][2].append(tracker)
                            else:
                                uncomplete_trackers[freq_bracket] = [start_date, end_date, [tracker]]

                            eval(f"uncomplete_{freq_bracket}").append(tracker)
                        if isinstance(tracker, TrackerMinAim):
                            if "TrackerMinAim" in lever_trackers.keys():
                                lever_trackers["TrackerMinAim"].append(tracker)
                            else:
                                lever_trackers["TrackerMinAim"] = [tracker]
                        if isinstance(tracker, TrackerBoolean):
                            if "TrackerBoolean" in lever_trackers.keys():
                                lever_trackers["TrackerBoolean"].append(tracker)
                            else:
                                lever_trackers["TrackerBoolean"] = [tracker]

            # Build the context dictionary
                    aim_levers[lever] = lever_trackers
                all_cat_aim_data[aim] = aim_levers
            aims_by_cat.append((full_cat_path, all_cat_aim_data))
        context['uncomplete_trackers'] = uncomplete_trackers
        context['aims_by_cat'] = sorted(aims_by_cat)
        context['min_aim_form'] = TrackerMinAimRecordsForm(self.request.POST)
        context['boolean_form'] = TrackerBooleanRecordsForm(self.request.POST)
        return context

    def form_valid(self, form):
        #self.in_category = get_object_or_404(DevelopmentCategory, id=SkillArea.objects.filter(skill_area_name=self.kwargs['dev_area_name'])[0].id)
        form.instance.tracker = self.request.POST.get("tracker_id")
        form.instance.lever_peformed = True
        return super().form_valid(form)

    def post(self, form):
        print(self.request.POST)
        if "TrackerMinAim" in self.request.POST:
            get_tracker = get_object_or_404(TrackerMinAim, id=self.request.POST.get('tracker_id'))
            new_log = TrackerMinAimRecords(
                    tracker = get_tracker,
                    lever_performed = True,
                    metric_quantity = self.request.POST.get("metric_quantity")
            )
            new_log.save()
            print("yoyoyo")
            return HttpResponseRedirect(f"/aims_dash/#QAloc_{self.request.POST.get('for_period')}")
        elif "TrackerBoolean" in self.request.POST:
            get_tracker = get_object_or_404(TrackerBoolean, id=self.request.POST.get('tracker_id'))
            new_log = TrackerBooleanRecords(
                    tracker = get_tracker,
                    lever_performed = True,
                    metric_quantity = self.request.POST.get("metric_quantity")
            )
            new_log.save()
            print(f"/aims_dash/#QAloc_{self.request.POST.get('for_period')}")
            return HttpResponseRedirect(f"/aims_dash/#QAloc_{self.request.POST.get('for_period')}")
        else:
            print("doesnt work")
            return HttpResponseRedirect('/aims_dash/')


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
                start_date = reset_user_time - time_delta(hours=24)
                end_date =  reset_user_time - time_delta(seconds=1)
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
