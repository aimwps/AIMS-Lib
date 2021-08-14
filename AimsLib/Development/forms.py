from django import forms
from .models import Aim, Lever, TrackerMinAim, TrackerMinAimRecords, TrackerBoolean, TrackerBooleanRecords, DevelopmentCategory
from bootstrap_datepicker_plus import DatePickerInput

class TrackerBooleanNewForm(forms.ModelForm):
    class Meta:
        model = TrackerMinAim
        fields = ('metric_description', 'frequency', 'frequency_quantity','start_date', 'end_date', 'complete_value', 'complete_criteria')
        widgets = {

                'metric_description': forms.TextInput(attrs = {
                                            'class': 'form-control',
                                            'placeholder': 'Action e.g. "exercise", "smoke", "run", "study" '}),

                'frequency':  forms.Select(attrs = {
                                            'class': 'form-control',
                                            'placeholder': 'Frequency: How often to track'}),

                'frequency_quantity':  forms.TextInput(attrs = {
                                            'class': 'form-control',
                                            'placeholder': 'Frequency: How often per period'}),

                'complete_criteria':  forms.Select(attrs = {
                                            'class': 'form-control'}),

                'complete_value': forms.TextInput(attrs = {
                                            'class': 'form-control',
                                            'placeholder': '30'}),

                'start_date': DatePickerInput(attrs = {
                                            'class': 'form-control',
                                            'placeholder': 'Tracking will commence on..'}),

                'end_date':DatePickerInput( attrs = {
                                            'class': 'form-control',
                                            'placeholder': 'Until the end of time. (or select a date)'}),

                }

class TrackerBooleanRecordsForm(forms.ModelForm):
    class Meta:
        model = TrackerBooleanRecords
        fields = ("metric_quantity",)
        widgets = {
            'metric_quantity': forms.Select(attrs = {
                                        'class': 'form-control',}),
            }



class TrackerMinAimNewForm(forms.ModelForm):
    class Meta:
        model = TrackerMinAim
        fields = ('metric_type', 'metric_min', 'metric_aim','metric_description', 'frequency', 'frequency_quantity','start_date', 'end_date', 'complete_value', 'complete_criteria')
        widgets = {
                'metric_type': forms.TextInput(attrs = {
                                            'class': 'form-control',
                                            'placeholder': 'Metric type e.g. "miles", "cigarettes", "calories", "minutes", "hours"'},
                                            ),

                'metric_min': forms.TextInput(attrs = {
                                            'class': 'form-control',
                                            'placeholder': 'Minimum Show e.g. "5" (minutes exercise)'},
                                            ),

                'metric_aim':forms.TextInput(attrs = {
                                            'class': 'form-control',
                                            'placeholder': 'On Track e.g. "20" (minutes exercise)'}),

                'metric_description': forms.TextInput(attrs = {
                                            'class': 'form-control',
                                            'placeholder': 'Action e.g. "exercise", "smoke", "run", "study" '}),

                'frequency':  forms.Select(attrs = {
                                            'class': 'form-control',
                                            'placeholder': 'Frequency: How often to track'}),

                'frequency_quantity':  forms.TextInput(attrs = {
                                            'class': 'form-control',
                                            'placeholder': 'Frequency: How often per period'}),

                'complete_criteria':  forms.Select(attrs = {
                                            'class': 'form-control'}),

                'complete_value': forms.TextInput(attrs = {
                                            'class': 'form-control',
                                            'placeholder': '30'}),

                'start_date': DatePickerInput(attrs = {
                                            'class': 'form-control',
                                            'placeholder': 'Tracking will commence on..'}),

                'end_date':DatePickerInput( attrs = {
                                            'class': 'form-control',
                                            'placeholder': 'Until the end of time. (or select a date)'}),

                }


class TrackerMinAimRecordsForm(forms.ModelForm):
    class Meta:
        model = TrackerMinAimRecords
        fields = ("metric_quantity",)
        widgets = {
            'metric_quantity': forms.TextInput(attrs = {'class': 'form-control'}),
            }

class LeverNewForm(forms.ModelForm):
    class Meta:
        model = Lever
        fields = ('description',)
        widgets = {
            'description': forms.TextInput(attrs = {'class': 'form-control'}),}

class AimNewForm(forms.ModelForm):
    class Meta:
        model = Aim
        fields = ('category','title', 'why')
        widgets = {
            'category': forms.Select(attrs = {'class': 'form-control'}),
            'title': forms.Textarea(attrs = {'class': 'form-control',
            'placeholder': 'A description of your aim',
            'rows':3,}),
            'why': forms.Textarea(attrs = {'class': 'form-control',
            'placeholder': "Why are you aiming for this? You should go into great detail here. You can also add to it later."}),}
    def __init__(self, *args, **kwargs):
        super(AimNewForm, self).__init__(*args, **kwargs)
        # this is pseudo code but you should get all variants
        # then get the product related to each variant
        dev_cats = DevelopmentCategory.objects.all()
        categories = sorted([(cat.id, str(cat)) for cat in dev_cats], key=lambda x: x[1])
        self.fields['category'].choices = categories
