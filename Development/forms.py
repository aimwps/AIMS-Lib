from django import forms
from .models import Aim, Behaviour, StepTracker
from Interactions.models import ContentCategory
from bootstrap_datepicker_plus import DatePickerInput


class StepTrackerCreateForm(forms.ModelForm):
    class Meta:
        model = StepTracker
        fields = (
                "metric_tracker_type",
                "metric_action",
                "metric_unit",
                "metric_int_only",
                "metric_min",
                "metric_max",
                "minimum_show_allowed",
                "minimum_show_description",
                "record_start_date",
                "record_frequency",
                "record_multiple_per_frequency",
                "complete_allowed",
                "complete_criteria",
                "complete_value",)
        widgets = {
                "metric_tracker_type": forms.Select(attrs={'class': 'form-control', 'placeholder': 'type of tracker'}),
                "metric_action": forms.TextInput(attrs={'class': 'form-control', 'placeholder':'The action you are taking, usually a verb e.g. run or perform',}),
                "metric_unit":forms.TextInput(attrs={'class': 'form-control', 'placeholder':'The unit type your recording e.g. hours, miles, grams, repititions',}),
                "metric_int_only":forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                "metric_min":forms.TextInput(attrs={'class': 'form-control', 'placeholder':'The lowest expectation of your unit actions',}),
                "metric_max":forms.TextInput(attrs={'class': 'form-control', 'placeholder':'The kick-ass expectation of your unit actions',}),
                "minimum_show_allowed":forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                "minimum_show_description":forms.TextInput(attrs={'class': 'form-control', 'placeholder':'A statement you perform as an aboslutley bare minimum to keep you in the game',}),
                "record_start_date":DatePickerInput(attrs = {'class': 'form-control','placeholder': 'Tracking will commence on..'}),
                "record_frequency":forms.Select(attrs={'class': 'form-control'}),
                "record_multiple_per_frequency":forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                "complete_allowed":forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                "complete_criteria": forms.Select(attrs={"class": 'form-control'}),
                "complete_value":forms.TextInput(attrs={'class': 'form-control', 'placeholder':"How many times you'll complete this to know it's engrained",}),
        }
    def __init__(self, *args, **kwargs):
        super(StepTrackerCreateForm, self).__init__(*args, **kwargs)
        self.initial['metric_tracker_type'] = 'boolean'
        self.initial['record_frequency'] = 'weekly'



class BehaviourCreateForm(forms.ModelForm):
    class Meta:
        model = Behaviour
        fields = ('title',)
        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control',
                                                    'placeholder': 'Enter your new behaviour here - e.g. "I go to the gym" or "I do not smoke cigarettes"',
                                                    }),}
class BehaviourEditForm(forms.ModelForm):
    class Meta:
        model = Behaviour
        fields = ('title',)
        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control',
                                                    'placeholder': 'Enter your new behaviour here - e.g. "I go to the gym" or "I do not smoke cigarettes"',
                                                    }),}

class AimCreateForm(forms.ModelForm):
    class Meta:
        model = Aim
        fields = ('category','title', 'motivation')
        widgets = {
            'category': forms.Select(attrs = {'class': 'form-control'}),
            'title': forms.Textarea(attrs = {'class': 'form-control',
            'placeholder': 'A description of your aim',
            'rows':3,}),
            'motivation': forms.Textarea(attrs = {'class': 'form-control',
            'placeholder': "Why are you aiming for this? You should go into great detail here. You can also add to it later."}),}
    def __init__(self, *args, **kwargs):
        super(AimCreateForm, self).__init__(*args, **kwargs)
        # this is pseudo code but you should get all variants
        # then get the product related to each variant
        dev_cats = ContentCategory.objects.all()
        categories = sorted([(cat.id, str(cat)) for cat in dev_cats], key=lambda x: x[1])
        self.fields['category'].choices = categories
