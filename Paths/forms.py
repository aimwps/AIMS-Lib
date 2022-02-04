from django import forms
from .models import Pathway, PathwayContent, PathwayCost
class PathwayCostCreateForm(forms.ModelForm):
    class Meta:
        model = PathwayCost
        fields = (
                    "pathway",
                    "purchase_quantity",
                    "purchase_cost",
                    )
        widgets = {
            "pathway": forms.TextInput(attrs = {'class': 'form-control', "type":"hidden"}),
            "purchase_quantity": forms.TextInput(attrs = {'class': 'form-control'}),
            "purchase_cost" :forms.TextInput(attrs = {'class': 'form-control'}),
                                            }


class PathwayContentEditForm(forms.ModelForm):
    class Meta:
        model = PathwayContent
        fields = (  "complete_to_move_on",
                    "complete_anytime_overide",
                    "revise_frequency",)
        widgets ={
            'complete_to_move_on': forms.CheckboxInput(attrs = {'class': 'form-check-input'}),
            'complete_anytime_overide': forms.CheckboxInput(attrs = {'class': 'form-check-input'}),
            'revise_frequency': forms.Select(attrs={'class': 'form-control'}
                                            ),}
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
        fields = ('content_type', 'article', 'video', 'benchmark','complete_anytime_overide', 'complete_to_move_on', 'revise_frequency')
        widgets = {'content_type': forms.Select(attrs={'class': 'form-control'}),
                    'article': forms.Select(attrs={'class': 'form-control'}),
                    'video': forms.Select(attrs={'class': 'form-control'}),
                    'benchmark': forms.Select(attrs={'class': 'form-control'}),
                    'complete_anytime_overide': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                    'complete_to_move_on': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                    'revise_frequency': forms.Select(attrs={'class': 'form-control'})
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
