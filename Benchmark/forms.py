from django import forms
from .models import Quiz
from bootstrap_datepicker_plus import DatePickerInput



class BenchmarkNewForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('title',)
        widgets ={
            'title': forms.TextInput(attrs = {'class': 'form-control',
                                            'placeholder': 'Enter the title of your new benchmark'}),
            }
