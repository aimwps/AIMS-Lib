from django.shortcuts import render, get_object_or_404
from .models import Aim, Lever, TrackerMinAim, DevelopmentCategory
from .forms import AimNewForm, LeverNewForm, TrackerMinAimNewForm
from django.views.generic import TemplateView, CreateView, View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class TrackerMinAimNew(TemplateView):
    template_name = "tracker_min_aim.html"

    def form_valid(self, form):
        print("executed")
        form.instance.lever = Lever.objects.get(id=self.kwargs['lever_id'])
        # For getting and resetting the correct order
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        kwargs = super(TrackerSelect, self).get_context_data(**kwargs)
        # Your code here
        kwargs['foo'] = "bar"
        return kwargs
    def post(self, request, *args, **kwargs):
        print("Post was requeste")
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class TrackerSelect(TemplateView):
    template_name = "tracker_select.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['min_aim_form'] = TrackerMinAimNewForm()
        return context

    def form_valid(self, form):
        self.lever = get_object_or_404(Lever, id=self.kwargs['lever_id'])
        form.instance.lever = self.lever
        print(form)
        #messages.success(self.request, 'Your reply has been posted successfully')
        return super().form_valid(form)

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.method =="POST" and "min_aim_tracker_submit" in request.POST:
            print(self.kwargs)
            if context['min_aim_form'].is_valid():
                new_tracker = TrackerMinAim(lever = Lever.objects.get(id=self.kwargs['lever_id']),
                                            metric_type = context['min_aim_form'].cleaned_data.get('metric_type'),
                                            metric_min = context['min_aim_form'].cleaned_data.get('metric_min'),
                                            metric_aim = context['min_aim_form'].cleaned_data.get('metric_aim'),
                                            metric_description = context['min_aim_form'].cleaned_data.get('metric_description'),
                                            frequency = context['min_aim_form'].cleaned_data.get('frequency'),
                                            start_date = context['min_aim_form'].cleaned_data.get('start_date'),
                                            end_date = context['min_aim_form'].cleaned_data.get('end_date'),
                                            complete_criteria = context['min_aim_form'].cleaned_data.get('complete_criteria'),
                                            complete_value =context['min_aim_form'].cleaned_data.get('complete_value'))
                new_tracker.save()
                print(new_tracker)
                return HttpResponseRedirect(request.path)
            else:
                print(request.POST)
                print("\nERRORS")
                print(context['min_aim_form'].errors)

                print("\n non field error \n")

                print(context['min_aim_form'].non_field_errors)


        return self.render_to_response(context)




def SelectAssignTracker(request, lever_id):
    min_aim_form = TrackerMinAimNewForm(request.POST or None)#
    lever =  get_object_or_404(Lever,id=lever_id)
    template_name = "tracker_select.html"
    if request.method =="POST" and "min_aim_tracker_submit" in request.POST:
        print(request.POST)
        if min_aim_form.is_valid():
            new_tracker = TrackerMinAim(lever = Lever.objects.get(id=lever_id),
                                        metric_type = min_aim_form.cleaned_data.get('metric_type'),
                                        metric_min = min_aim_form.cleaned_data.get('metric_min'),
                                        metric_aim = min_aim_form.cleaned_data.get('metric_aim'),
                                        metric_description = min_aim_form.cleaned_data.get('metric_description'),
                                        frequency = min_aim_form.cleaned_data.get('frequency'),
                                        start_date = min_aim_form.cleaned_data.get('start_date'),
                                        end_date = min_aim_form.cleaned_data.get('end_date'),
                                        complete_criteria = min_aim_form.cleaned_data.get('complete_criteria'),
                                        complete_value = min_aim_form.cleaned_data.get('complete_value'))
            new_tracker.save()
            print(new_tracker)
            return HttpResponseRedirect(request.path)

    context = {"min_aim_form": min_aim_form}
    return render(request, template_name, context)



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
    template_name = "an_aim.html"
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
