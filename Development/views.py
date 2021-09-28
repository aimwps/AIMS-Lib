from django.shortcuts import render, get_object_or_404
from .models import Aim, Behaviour, StepTracker
from WebsiteTools.models import ContentCategory
from Members.models import MemberProfile
from .forms import AimCreateForm, BehaviourCreateForm, BehaviourEditForm
from django.views.generic import TemplateView, CreateView, View, UpdateView
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from django.db.models import Q
import calendar
from dateutil.relativedelta import relativedelta
from collections import OrderedDict
from django.contrib.auth.mixins import LoginRequiredMixin

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
    template_name = 'lever_edit.html'

class BehaviourCreate(LoginRequiredMixin, CreateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model = Behaviour
    form_class = BehaviourCreateForm
    template_name = "lever_new.html"

    def form_valid(self, form):
        #self.in_category = get_object_or_404(ContentCategory, id=SkillArea.objects.filter(skill_area_name=self.kwargs['dev_area_name'])[0].id)
        form.instance.on_aim = Aim.objects.get(id=self.kwargs['aim_id'])
        # For getting and resetting the correct order
        all_aim_levers = Behaviour.objects.filter(on_aim=self.kwargs['aim_id']).order_by('in_order')

        for i, lever in  enumerate(all_aim_levers):
            lever.in_order =  i
            lever.save()
        form.instance.in_order = len(all_aim_levers)
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
        form.instance.user = self.request.user
        all_user_aims = Aim.objects.filter(user=self.request.user).order_by("in_order")
        for i, aim in enumerate(all_user_aims):
            aim.in_order = i
            aim.save()
        form.instance.in_order = (len(all_user_aims))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            nav_data = ModuleNavData.objects.filter(module_sub_page=self.template_name)
        except:
            nav_data = None

        if nav_data:
            context['nav_data'] = nav_data[0]
        return context

class AimView(LoginRequiredMixin, TemplateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "aims.html"
    #form_class = ForumTopicNewComment
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aims = []
        for aim in Aim.objects.filter(user=self.request.user.id):
            aims.append(aim)
        context['aims_list'] = aims
        return context


class AimsDash(LoginRequiredMixin, TemplateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "aims_dash.html"
    #form_class = ForumTopicNewComment
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            nav_data = ModuleNavData.objects.filter(module_sub_page=self.template_name)
        except:
            nav_data = None

        if nav_data:
            context['nav_data'] = nav_data[0]

        #### Check if user has profile and load if so.
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'profile'):
                context['user_profile'] = MemberProfile.objects.get(user_profile=self.request.user.id)
                context['has_user_profile'] = True
            else:
                context['has_user_profile'] = False

            #### Get aLL the users aims
            user_aims = Aim.objects.filter(user=self.request.user)
            user_aims_behaviours = {aim: list(Behaviour.objects.filter(on_aim=aim)) for aim in user_aims}
            user_all_aims = {}
            for aim, behaviours in user_aims_behaviours.items():
                trackers_behaviours = {}
                for behaviour in behaviours:
                    trackers_behaviours[behaviour] = behaviour.get_trackers()
                user_all_aims[aim] = trackers_behaviours
            aims_cat = [(str(aim.category), aim.in_order, aim.title, aim.why, {aim:behaviour}) for aim, behaviour in user_all_aims.items()]
            sorted_aims = sorted(aims_cat, key=lambda x:x[1])
            context['sorted_aims'] = sorted_aims




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


    # Get all trackers
        if self.request.user.is_authenticated:
            all_behaviours  = Behaviour.objects.filter(on_aim__user=self.request.user)
            for behaviour in all_behaviours:
                trackers = behaviour.get_trackers()
                for tracker in trackers:
                    tracker_complete, freq_bracket, start_date, end_date = self.check_tracker_status(tracker)
                    if not tracker_complete:
                        if uncomplete_trackers[freq_bracket] != None:
                            uncomplete_trackers[freq_bracket][2].append(tracker)
                        else:
                            uncomplete_trackers[freq_bracket] = [start_date, end_date, [tracker]]

                        eval(f"uncomplete_{freq_bracket}").append(tracker)
        context['uncomplete_trackers'] = uncomplete_trackers
        context['min_aim_form'] = TrackerMinAimRecordsForm(self.request.POST)
        context['boolean_form'] = TrackerBooleanRecordsForm(self.request.POST)

        return context

    def form_valid(self, form):
        form.instance.tracker = self.request.POST.get("tracker_id")
        form.instance.lever_peformed = True
        return super().form_valid(form)

    def post(self, form):
        if "TrackerMinAim" in self.request.POST:
            get_tracker = get_object_or_404(TrackerMinAim, id=self.request.POST.get('tracker_id'))
            if self.request.POST.get("TrackerMinAim") == "dnc":
                tcompleted = False
            else:
                tcompleted=True
            new_log = TrackerMinAimRecords(
                    tracker = get_tracker,
                    lever_performed = tcompleted,
                    metric_quantity = self.request.POST.get("metric_quantity")
            )
            new_log.save()
            return HttpResponseRedirect(f"/aims_dash/#QAloc_{self.request.POST.get('for_period')}")
        elif "TrackerBoolean" in self.request.POST:
            get_tracker = get_object_or_404(TrackerBoolean, id=self.request.POST.get('tracker_id'))
            if self.request.POST.get("TrackerBoolean") == "dnc":
                tcompleted = False
            else:
                tcompleted=True
            new_log = TrackerBooleanRecords(
                    tracker = get_tracker,
                    lever_performed = tcompleted,
                    metric_quantity = self.request.POST.get("metric_quantity")
            )
            new_log.save()
            return HttpResponseRedirect(f"/aims_dash/#QAloc_{self.request.POST.get('for_period')}")

        elif "delete_behaviour" in self.request.POST:
            get_lever = get_object_or_404(Behaviour, id=self.request.POST.get('delete_behaviour'))
            get_lever.user_status = "deleted"
            get_lever.save()
            return HttpResponseRedirect('/aims_dash/#myaims')

        elif "delete_aim" in self.request.POST:
            get_aim = get_object_or_404(Aim, id=self.request.POST.get("delete_aim"))
            get_aim.user_status = "deleted"
            get_aim.save()
            return HttpResponseRedirect('/aims_dash/#myaims')
        elif "delete_tracker" in self.request.POST:
            tclass = self.request.POST.get("delete_tclass")
            tracker = get_object_or_404(eval(tclass), id=self.request.POST.get("delete_tracker"))
            tracker.user_status = "deleted"
            tracker.save()
            return HttpResponseRedirect('/aims_dash/#myaims')
        else:
            return HttpResponseRedirect('/aims_dash/#myaims')


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
