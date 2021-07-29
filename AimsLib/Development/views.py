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
        print(context)
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
                print("Form not valid")
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
        print(all_aim_levers)
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
        # of style [(cat_path, cat_aims)]
        trackers = Aim.check_aim_trackers(self.request.user.id)
        print("TRACKERS HERE ")
        print(trackers)
        aims_by_cat = []
        for cat in DevelopmentCategory.objects.all():
            all_cat_aim_data = {}
            full_cat_path = get_category_path(cat)
            cat_aims = Aim.objects.filter(user=self.request.user.id, category=cat.id)

            for aim in cat_aims:
                aim_levers = {}
                all_aim_levers = Lever.objects.filter(on_aim = aim.id).order_by("in_order")
                for lever in all_aim_levers:
                    lever_trackers = {}
                    trackers = lever.get_trackers()
                    for tracker in trackers:
                        self.check_tracker_status(tracker)
                        if isinstance(tracker, TrackerMinAim):
                            if "TrackerMinAim" in lever_trackers.keys():
                                lever_trackers["TrackerMinAim"].append(tracker)
                            else:
                                lever_trackers["TrackerMinAim"] = [tracker]
                    aim_levers[lever] = lever_trackers
                all_cat_aim_data[aim] = aim_levers
            aims_by_cat.append((full_cat_path, all_cat_aim_data))
        context['aims_by_cat'] = sorted(aims_by_cat)

        return context

    def check_tracker_status(self, tracker):

        if isinstance(tracker, TrackerMinAim):
            tracker_logs = MinAimRecords.objects.filter(tracker=tracker.id).order_by('record_date', 'record_time')
            #most_recent = tracker_logs[0]
            if tracker.day_reset_on == "midnight":
                reset_time = datetime(1800, 12, 25, 0,0,0,0).time()
            else:
                reset_time = MemberProfile.objects.get(user_profile=self.request.user.id).day_reset_time

            if tracker.frequency == 'hourly':
                pass
            elif tracker.frequency =='daily':
                current_period_start, current_period_end = self.create_range_time(datetime.today(), datetime.today(), reset_time)
                print(current_period_start, current_period_end)


            elif 'week' in tracker.frequency:
                if tracker.week_reset_on == "start date day":
                    week_reset_day = tracker.start_date.weekday()#strftime('%A')
                    if week_reset_day == datetime.today.weekday():
                        if tracker.day_reset == 'midnight':
                            pass
                    current_period_start = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
                    current_period_end = datetime.today().replace(hour=23, minute=59, second=59, microsecond=0)
                else:
                    pass

            else:
                current_period = datetime.today()
                print(current_period)

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
