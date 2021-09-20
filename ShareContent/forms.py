from django import forms
from .models import UserCreatedGroup, UserCreatedGroupContent
from bootstrap_datepicker_plus import DatePickerInput
from Paths.models import Pathway

class UserGroupCreateForm(forms.ModelForm):
    class Meta:
        model =  UserCreatedGroup
        fields = ("name", "members")
        widgets = {
            'name': forms.TextInput(attrs = {'class': 'form-control',
                                            'placeholder': 'The name of your group..'}),
            'members': forms.SelectMultiple(attrs = {'class': 'form-control',
                                            }),

        }

class UserGroupEditForm(forms.ModelForm):
    class Meta:
        model =  UserCreatedGroup
        fields = ("name", "members")
        widgets = {
            'name': forms.TextInput(attrs = {'class': 'form-control',
                                            'placeholder': 'The name of your group..'}),
            'members': forms.SelectMultiple(attrs = {'class': 'form-control',
                                            }),
        }


class UserGroupPathwayCreateForm(forms.ModelForm):
    class Meta:
        model =  UserCreatedGroupContent
        fields = ("content_id",)
    def __init__(self, user=None, *args,**kwargs):
        super(UserGroupPathwayCreateForm, self).__init__(*args, **kwargs)
        user_pathways = sorted([(pathway.id, str(pathway.title)) for pathway in Pathway.objects.filter(author=user)])
        self.fields['content_id'].choices = user_pathways

class UserGroupPathwayEditForm(forms.ModelForm):
    class Meta:
        model =  UserCreatedGroupContent
        fields = ("content_id",)
    def __init__(self, user=None, *args,**kwargs):
        super(UserGroupPathwayEditForm, self).__init__(*args, **kwargs)
        user_pathways = sorted([(pathway.id, str(pathway.title)) for pathway in Pathway.objects.filter(author=user)])
        self.fields['content_id'].choices = user_pathways
