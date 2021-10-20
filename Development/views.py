from django.shortcuts import render, get_object_or_404
from .models import Aim, Behaviour, StepTracker, StepTrackerLog, StepTrackerCustomFrequency
from WebsiteTools.models import ContentCategory
from Members.models import MemberProfile
from .forms import AimCreateForm, BehaviourCreateForm, BehaviourEditForm, StepTrackerCreateForm
from django.views.generic import TemplateView, CreateView, View, UpdateView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse
from datetime import datetime, timedelta
from django.db.models import Q
import json
from dateutil.relativedelta import relativedelta
from collections import OrderedDict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .utils import prettify_tracker_log_dict
from .development_serializers import StepTrackerSerializer

def test_data_entry(tracker):
    query = StepTrackerLog.objects.filter(on_tracker=tracker).order_by('create_date')
    for q in query:
        print(q.create_date, q.count_value, q.id)
    return query

def submit_tracker_log(request):
    tracker = get_object_or_404(StepTracker, id=request.POST.get("tracker_id"))
    submit_user = get_object_or_404(User, id=request.POST.get("submit_user"))
    if request.POST.get("submit_value"):
        submit_value = request.POST.get("submit_value")
    else:
        submit_value = None
    new_log = StepTrackerLog(author=submit_user,
                            on_tracker=tracker,
                            submit_type=request.POST.get("submit_type"),
                            count_value=submit_value)
    new_log.save()
    response = json.dumps({"complete":True})
    return HttpResponse(response)

def get_tracker_period(start_date, end_date):
    now = datetime.today()
    in_future = relativedelta(end_date, start_date).days
    if in_future  <= 0:
        return "displayToday"
    elif in_future <= 6:
        return "displayWeek"
    elif in_future <= 31:
        return "displayMonth"
    else:
        return "displayYear"

def get_tracker_status(user_id, tracker):
    abc = test_data_entry(tracker)
    member_profile = MemberProfile.objects.get(author=user_id)
    tracker_info  = {'tracker':tracker,}
    now = datetime.today()
    reset_user_time = datetime.combine(now, member_profile.day_reset_time)
    reset_user_date_time = reset_user_time + relativedelta(day=member_profile.month_reset_day)
    reset_user_year_date_time = reset_user_date_time + relativedelta(month=member_profile.year_reset_month)
    start_datetimes = []
    end_datetimes = []
    all_upcoming_trackers = []
    ### Set the start and end date range for tracker filter based on the frequency of the tracker
    if tracker.record_frequency == "daily":
        if now > reset_user_time:
            start_date = reset_user_time
            end_date =  reset_user_time + timedelta(hours=23, minutes=59, seconds=59)
        else:
            start_date = reset_user_time - timedelta(hours=24)
            end_date =  reset_user_time - timedelta(seconds=1)
        start_datetimes.append(start_date)
        end_datetimes.append(end_date)

    if tracker.record_frequency == "weekly":
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
        start_datetimes.append(start_date)
        end_datetimes.append(end_date)

    if tracker.record_frequency == "monthly":
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
        start_datetimes.append(start_date)
        end_datetimes.append(end_date)

    if tracker.record_frequency == "yearly":
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
        start_datetimes.append(start_date)
        end_datetimes.append(end_date)

    if tracker.record_frequency == "custom":
        all_custom_freq_code = list(StepTrackerCustomFrequency.objects.filter(on_tracker=tracker))
        for freq_code in all_custom_freq_code:

    ### Set start and end period times for a specific day of the week, still uses the users daily reset time.
            if freq_code.code in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                temp_reset_user_time = reset_user_time
                while temp_reset_user_time.strftime('%A') != freq_code.code:

                    temp_reset_user_time += relativedelta(days=1)
                if now > reset_user_time:
                    start_date = temp_reset_user_time
                    end_date =  temp_reset_user_time + timedelta(hours=23, minutes=59, seconds=59)
                else:
                    start_date = temp_reset_user_time - timedelta(hours=24)
                    end_date =  temp_reset_user_time - timedelta(seconds=1)
                start_datetimes.append(start_date)
                end_datetimes.append(end_date)
    ### Set start and end period times for a specific month of the year, still uses the monthly reset day.
            elif freq_code.code in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]:
                temp_reset_user_time = reset_user_time
                while temp_reset_user_time.strftime('%B') != freq_code.code:

                    temp_reset_user_time += relativedelta(months=1)
                if now > temp_reset_user_time:
                    start_date = temp_reset_user_time
                    end_date =  temp_reset_user_time + relativedelta(months=1) - timedelta(seconds=1)
                else:
                    start_date = temp_reset_user_time - relativedelta(months=1)
                    end_date =  temp_reset_user_time - timedelta(seconds=1)
                start_datetimes.append(start_date)
                end_datetimes.append(end_date)
    ### Set start and end period times for a specific day in the month, e.g. "the 12th of every month". Still users the daily reset time.
            else:
                temp_reset_user_time = reset_user_time
                while temp_reset_user_time.strftime('%-d') != freq_code.code:

                    temp_reset_user_time += relativedelta(days=1)
                if now > reset_user_time:
                    start_date = temp_reset_user_time
                    end_date =  temp_reset_user_time + timedelta(hours=23, minutes=59, seconds=59)
                else:
                    start_date = temp_reset_user_time - timedelta(hours=24)
                    end_date =  temp_reset_user_time - timedelta(seconds=1)
                start_datetimes.append(start_date)
                end_datetimes.append(end_date)


        min_start_date = min(start_datetimes)
        period_index = start_datetimes.index(min_start_date)
        start_date =  start_datetimes[period_index]
        end_date = end_datetimes[period_index]

    #for start_date, end_date in zip(start_datetimes, end_datetimes):
        ## RETURN DICTIONARY OF TRACKER INFO
    current_period_logs = StepTrackerLog.objects.filter(on_tracker=tracker.id, create_date__range=[start_date, end_date])

    total_logs = len(current_period_logs)
    tracker_status ={
            "tracker": tracker,
            "logs_required": None,
            "total_logs": total_logs,
            "period_log_start": start_date,
            "period_log_end": end_date,
            "boolean_status": None,
            "count_status": None,
            "count_quantity": None,
            "count_total": None,
            }

    if current_period_logs:
        logs_status = list(current_period_logs.values_list('submit_type', flat=True))

        if tracker.metric_tracker_type == "boolean":
            if "min_showup" in logs_status or "fail_or_no_submit" in logs_status or "boolean_success" in logs_status:
                tracker_status['logs_required'] = False
                tracker_status['boolean_status'] = logs_status[0]
            else:
                tracker_status['logs_required'] = True
                tracker_status['boolean_status'] = logs_status[0]
        else:
            if "min_showup" in logs_status or "fail_or_no_submit" in logs_status:
                tracker_status['logs_required'] = False
                tracker_status['count_status'] = logs_status[0]
            else:
                value_counts = list(current_period_logs.values_list('count_value', flat=True))
                sum_counts = sum([int(i) for i in value_counts if i != None])
                tracker_status['logs_required'] = True
                tracker_status['count_total'] = sum_counts
                tracker_status['boolean_status'] = logs_status[0]
                tracker_status['count_quantity'] = len(value_counts)
    else:
        tracker_status['logs_required'] = True
    #all_upcoming_trackers.append(tracker_status)

    return tracker_status

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

def request_uncomplete_trackers(request):
    all_user_trackers = list(StepTracker.objects.filter(Q(on_behaviour__on_aim__author=request.GET.get("user_id")) & Q(user_status="active") & Q(record_start_date__lte=datetime.today())))
    uncomplete_trackers = []
    for tracker in all_user_trackers:
        tracker_status = get_tracker_status(request.GET.get("user_id"), tracker)

        if tracker_status['logs_required']:
            tracker_status['display_section'] = get_tracker_period(tracker_status['period_log_start'], tracker_status['period_log_end'])
            serialize_tracker = StepTrackerSerializer(tracker_status['tracker']).data
            tracker_status['tracker'] = serialize_tracker
            tracker_status['question'] = tracker.get_tquestion()
            tracker_status['pretty_start'] = tracker_status['period_log_start'].strftime("%d/%m/%y @ %H:%M:%S")
            tracker_status['pretty_end'] = tracker_status['period_log_end'].strftime("%d/%m/%y @ %H:%M:%S")
            uncomplete_trackers.append(tracker_status)
    return JsonResponse(uncomplete_trackers, safe=False)

class StepTrackerCreate(LoginRequiredMixin,CreateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    form_class = StepTrackerCreateForm
    model = StepTracker
    template_name = "steptracker_create.html"


    def get_success_url(self):
        return reverse("aims-dash")

    def form_valid(self, form):
        form.instance.on_behaviour = get_object_or_404(Behaviour, id=self.kwargs['behaviour_id'])
        all_behaviour_trackers =  StepTracker.objects.filter(on_behaviour=self.kwargs['behaviour_id']).order_by('order_position')
        for i, tracker in  enumerate(all_behaviour_trackers):
            tracker.order_position =  i
            tracker.save()
        form.instance.order_position = len(all_behaviour_trackers)
        response = super().form_valid(form)
        if form.instance.record_frequency == "custom":
            for key in self.request.POST:
                if "customFreqCode" in key:
                    code = key.replace("customFreqCode_", "")
                    new_freq = StepTrackerCustomFrequency(on_tracker=form.instance, code=code)
                    new_freq.save()
        return response

class AimEdit(LoginRequiredMixin, UpdateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model= Aim
    form_class = AimCreateForm
    template_name = 'aim_edit.html'

class BehaviourEdit(LoginRequiredMixin, UpdateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model= Behaviour
    form_class = BehaviourEditForm
    template_name = 'behaviour_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aim_for_lever'] = Aim.objects.get(id=self.kwargs['pk'])
        return context

class BehaviourCreate(LoginRequiredMixin, CreateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model = Behaviour
    form_class = BehaviourCreateForm
    template_name = "behaviour_create.html"
    def form_valid(self, form):
        #self.in_category = get_object_or_404(ContentCategory, id=SkillArea.objects.filter(skill_area_name=self.kwargs['dev_area_name'])[0].id)
        form.instance.on_aim = Aim.objects.get(id=self.kwargs['aim_id'])
        # For getting and resetting the correct order
        all_aim_levers = Behaviour.objects.filter(on_aim=self.kwargs['aim_id']).order_by('order_position')

        for i, lever in  enumerate(all_aim_levers):
            lever.order_position =  i
            lever.save()
        form.instance.order_position = len(all_aim_levers)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aim_for_lever'] = Aim.objects.get(id=self.kwargs['aim_id'])
        return context

class AimCreate(LoginRequiredMixin, CreateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model = Aim
    form_class = AimCreateForm
    template_name = "aim_new.html"
    def form_valid(self, form):
        #self.in_category = get_object_or_404(ContentCategory, id=SkillArea.objects.filter(skill_area_name=self.kwargs['dev_area_name'])[0].id)
        form.instance.author = self.request.user
        all_user_aims = Aim.objects.filter(author=self.request.user).order_by("order_position")
        for i, aim in enumerate(all_user_aims):
            aim.order_position = i
            aim.save()
        form.instance.order_position = (len(all_user_aims))



        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AimView(LoginRequiredMixin, TemplateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "aims.html"
    #form_class = ForumTopicNewComment
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aims = []
        for aim in Aim.objects.filter(author=self.request.user.id):
            aims.append(aim)
        context['aims_list'] = aims
        return context

class AimsDash(LoginRequiredMixin, TemplateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "aims_dash.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #### Check if user has profile and load if so.
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'profile'):
                context['user_profile'] = MemberProfile.objects.get(author=self.request.user.id)
                context['has_user_profile'] = True
            else:
                context['has_user_profile'] = False
        ########## Get aLL the users aims, behaviours & trackers######################################################
        if self.request.user.is_authenticated:
            user_aims = Aim.objects.filter(Q(author=self.request.user) & ~Q(user_status="deleted"))
            user_aims_behaviours = {aim: list(Behaviour.objects.filter(on_aim=aim)) for aim in user_aims}
            user_all_aims = {}
            for aim, behaviours in user_aims_behaviours.items():
                trackers_behaviours = {}

                ## For each behaviour find the trackers details
                for behaviour in behaviours:
                    all_behaviour_trackers = StepTracker.objects.filter(Q(on_behaviour=behaviour.id) & Q(user_status="active") & Q(record_start_date__lte=datetime.today()))

                    ## Pass trackers that need logs to uncomplete_trackers for quick fire aims
                    processed_trackers = []
                    for tracker in all_behaviour_trackers:
                        tracker_status = get_tracker_status(self.request.user.id, tracker)
                        processed_trackers.append((tracker, prettify_tracker_log_dict(tracker_status)))

                    ## Assign the trackers to the behaviours for viewing aims dash.
                    trackers_behaviours[behaviour] = processed_trackers

                user_all_aims[aim] = trackers_behaviours
            aims_cat = [(str(aim.category), aim.order_position, aim.title, aim.motivation, {aim:behaviour}) for aim, behaviour in user_all_aims.items()]
            sorted_aims = sorted(aims_cat, key=lambda x:x[1])
            context['sorted_aims'] = sorted_aims
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def post(self, form):
        if "delete_behaviour" in self.request.POST:
            get_lever = get_object_or_404(Behaviour, id=self.request.POST.get('delete_behaviour'))
            get_lever.user_status = "deleted"
            get_lever.save()
            return HttpResponseRedirect('/aims/#myaims')
        elif "delete_aim" in self.request.POST:
            get_aim = get_object_or_404(Aim, id=self.request.POST.get("delete_aim"))
            get_aim.user_status = "deleted"
            get_aim.save()
            return HttpResponseRedirect('/aims/#myaims')
        elif "delete_tracker" in self.request.POST:
            tracker = get_object_or_404(StepTracker, id=self.request.POST.get("delete_tracker"))
            tracker.user_status = "deleted"
            tracker.save()
            return HttpResponseRedirect('/aims/#myaims')
        else:
            return HttpResponseRedirect('/aims/#myaims')



## Check tracker history

# Given the record start date (or last_checked_date)
## and the frequency, find all possible logs from verification date until present date.
## Verify there is a log for them, if there is not a log, create one saying no entry.
