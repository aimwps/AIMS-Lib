from django import forms
from .models import Post


class ForumTopicNewForm(forms.ModelForm):
    class Meta:
        model= Post
        fields = ('title', 'skill_area', 'author', 'body')
        widgets ={
            'title': forms.TextInput(attrs = {'class': 'form-control'}),
            'skill_area': forms.TextInput(attrs = {'class': 'form-control'}),
            'author': forms.Select(attrs = {'class': 'form-control'}),
            'body': forms.Textarea(attrs = {'class': 'form-control'}),}
        # this is applying the css classes 'form-control' is predetermined
        # as we are using bootstrap, can reference any css assigned
class ForumTopicEditForm(forms.ModelForm):
    class Meta:
        model= Post
        fields = ('title', 'skill_area', 'body')
        widgets ={
            'title': forms.TextInput(attrs = {'class': 'form-control'}),
            'skill_area': forms.TextInput(attrs = {'class': 'form-control'}),
            'body': forms.Textarea(attrs = {'class': 'form-control'}),}
        # this is applying the css classes 'form-control' is predetermined
        # as we are using bootstrap, can reference any css assigned
