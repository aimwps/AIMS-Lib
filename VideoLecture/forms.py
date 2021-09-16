from django import forms
from .models import VideoLecture
from bootstrap_datepicker_plus import DatePickerInput


class VideoLectureNewForm(forms.ModelForm):
    class Meta:
        model =  VideoLecture
        fields = ('title','video_link','notes',)
        widgets ={
            'title': forms.TextInput(       attrs = {'class': 'form-control'}),
            'video_link': forms.TextInput(  attrs = {'class': 'form-control'}),
            'notes': forms.Textarea(        attrs = {
                                                'class': 'form-control',
                                                'row':4,
                                                }),
                                                }
