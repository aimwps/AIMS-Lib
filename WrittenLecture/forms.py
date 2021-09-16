from django import forms
from .models import WrittenLecture


class WrittenLectureEditForm(forms.ModelForm):
    class Meta:
        model = WrittenLecture
        fields = ('title',"body")
        widgets ={
            'title': forms.TextInput(attrs = {'class': 'form-control'}),
            'body': forms.Textarea(attrs = {'class': 'form-control',
                                            }),}

        # this is applying the css classes 'form-control' is predetermined
class WrittenLectureNewForm(forms.ModelForm):
    class Meta:
        model = WrittenLecture
        fields = ('title','body')
        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control'}),
            'body': forms.Textarea(attrs = {'class': 'form-control',}),
                }
