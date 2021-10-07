from django import forms
from .models import Benchmark
from bootstrap_datepicker_plus import DatePickerInput



class BenchmarkNewForm(forms.ModelForm):
    class Meta:
        model = Benchmark
        fields = ('title',)
        widgets ={
            'title': forms.TextInput(attrs = {'class': 'form-control',
                                            'placeholder': 'Enter the title of your new benchmark'}),
            }
