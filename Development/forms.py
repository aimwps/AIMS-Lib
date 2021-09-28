from django import forms
from .models import Aim, Behaviour, StepTracker
from Interactions.models import ContentCategory
from bootstrap_datepicker_plus import DatePickerInput



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
