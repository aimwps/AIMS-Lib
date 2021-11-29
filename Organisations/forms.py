from django import forms
from .models import Organisation, OrganisationContent
from bootstrap_datepicker_plus import DatePickerInput
from Paths.models import Pathway

class OrganisationCreateForm(forms.ModelForm):
    class Meta:
        model =  Organisation
        fields = ("title", "parent_organisation","members")
        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control',
                                            'placeholder': 'The name of your group..'}),
            'parent_organisation': forms.Select(attrs = {'class': 'form-control',
                                            }),
            'members': forms.SelectMultiple(attrs = {'class': 'form-control',
                                            }),

        }

class OrganisationEditForm(forms.ModelForm):
    class Meta:
        model =  Organisation
        fields = ("title","parent_organisation", "members")
        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control',
                                            'placeholder': 'The name of your group..'}),
            'members': forms.SelectMultiple(attrs = {'class': 'form-control',
                                            }),
        }



class OrganisationContentCreateForm(forms.ModelForm):
    class Meta:
        model =  OrganisationContent
        fields = ("content_type", "pathway")
        #widgets = {"content_id": forms.Select(attrs={"class": 'form-control'})}
    def __init__(self, user=None, *args,**kwargs):
        super().__init__(*args, **kwargs)
        user_pathways = sorted([(pathway.id, str(pathway.title)) for pathway in Pathway.objects.filter(author=user)])
        self.fields['content_id'].choices = ModelChoiceField()

class OrganisationContentEditForm(forms.ModelForm):
    class Meta:
        model =  OrganisationContent
        fields = ("content_type",)
        widgets = {"content_type": forms.Select(attrs={"class": 'form-control'})}
    # def __init__(self, user=None, *args,**kwargs):
    #     super().__init__(*args, **kwargs)
    #     user_pathways = sorted([(pathway.id, str(pathway.title)) for pathway in Pathway.objects.filter(author=user)])
    #     self.fields['content_id'].choices = user_pathways
    #     self.fields['content_id'].initial = user_pathways[0]
