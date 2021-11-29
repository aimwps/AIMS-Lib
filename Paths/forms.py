from django import forms
from .models import Pathway, PathwayContent


class PathwayEditForm(forms.ModelForm):
    class Meta:
        model = Pathway
        fields = ('title',"description")
        widgets ={
            'title': forms.TextInput(attrs = {'class': 'form-control'}),
            'description': forms.Textarea(attrs = {'class': 'form-control',
                                            }),}

class PathwayContentCreateForm(forms.ModelForm):
    class Meta:
        model =  PathwayContent
        fields = ('content_type', 'article', 'video', 'benchmark','revise_continuous', 'complete_previous')
        widgets = {'content_type': forms.Select(attrs={'class': 'form-control'}),
                    'article': forms.Select(attrs={'class': 'form-control'}),
                    'video': forms.Select(attrs={'class': 'form-control'}),
                    'benchmark': forms.Select(attrs={'class': 'form-control'}),
                    'revise_continuous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                    'complete_previous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PathwayCreateForm(forms.ModelForm):
    class Meta:
        model =  Pathway
        fields = ('title', 'description')
        widgets ={
            'title': forms.TextInput(attrs = {'class': 'form-control',
                                            'placeholder': 'The title of your pathway'}),
            'description': forms.Textarea(attrs = {'class': 'form-control',
                                                    'placeholder': 'A description of your pathway'}),}
