from django import forms
from .models import Aim, Lever, TrackerMinAim
from bootstrap_datepicker_plus import DatePickerInput

class TrackerMinAimNewForm(forms.ModelForm):
    class Meta:
        model = TrackerMinAim
        fields = ('metric_type', 'metric_min', 'metric_aim','metric_description', 'frequency', 'start_date', 'end_date', 'complete_value', 'complete_criteria')
        widgets = {
                'metric_type': forms.TextInput(attrs = {'class': 'form-control',
                                                        'placeholder': 'miles'}),
                'metric_min': forms.TextInput(attrs = {'class': 'form-control',
                                                        'placeholder': '1'}),
                'metric_aim':forms.TextInput(attrs = {'class': 'form-control',
                                                        'placeholder': '10'}),
                'metric_description': forms.TextInput(attrs = {'class': 'form-control',
                                                        'placeholder': 'run a minimum'}),
                'frequency':  forms.Select(attrs = {'class': 'form-control'}),
                'complete_criteria':  forms.Select(attrs = {'class': 'form-control'}),
                'complete_value': forms.TextInput(attrs = {'class': 'form-control',
                                                        'placeholder': '30'}),
                'start_date': DatePickerInput(attrs = {'class': 'form-control',
                                                        'placeholder': '27/08/2021'}),
                'end_date':DatePickerInput(), }

    # start_date = forms.DateField(widget = DatePicker())
    #

class LeverNewForm(forms.ModelForm):
    class Meta:
        model = Lever
        fields = ('description',)
        widgets = {
            'description': forms.TextInput(attrs = {'class': 'form-control'}),}

class AimNewForm(forms.ModelForm):
    class Meta:
        model = Aim
        fields = ('category', 'title', 'why')
        widgets = {
            'category': forms.Select(attrs = {'class': 'form-control'}),
            'title': forms.TextInput(attrs = {'class': 'form-control'}),
            #'author': forms.Select(attrs = {'class': 'form-control'}),
            'why': forms.Textarea(attrs = {'class': 'form-control'}),}
        # this is applying the css classes 'form-control' is predetermined
        # as we are using bootstrap, can reference any css assigned
class LeverNewForm(forms.ModelForm):
    class Meta:
        model = Lever
        fields = ('description',)
        widgets = {
            'description': forms.TextInput(attrs = {'class': 'form-control'}),}
