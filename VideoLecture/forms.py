from django import forms
from .models import VideoLecture, VideoLectureSession
from bootstrap_datepicker_plus import DatePickerInput


class VideoLectureNewForm(forms.ModelForm):
    class Meta:
        model =  VideoLecture
        fields = ('title','description','video_link','notes',)
        widgets ={
            'title': forms.TextInput(       attrs = {'class': 'form-control',
                                                    'placeholder': 'The title of this video'}),
            'description': forms.Textarea(        attrs = {
                                                'class': 'form-control',
                                                'row':2,
                                                'placeholder': 'Add a description'
                                                }),

            'video_link': forms.TextInput(  attrs = {'class': 'form-control',
                                                    'placeholder': 'Paste in video link here'}),

            'notes': forms.Textarea(        attrs = {
                                                'class': 'form-control',
                                                'row':4,
                                                'placeholder': 'Add any notes'
                                                }),
                                                }
class VideoLectureEditForm(forms.ModelForm):
    class Meta:
        model = VideoLecture
        fields = ('title','video_link','notes',)
        widgets ={
            'title': forms.TextInput(       attrs = {'class': 'form-control',
                                                    'placeholder': 'Give a title to the video'}),
            'video_link': forms.TextInput(  attrs = {'class': 'form-control',
                                                    'placeholder': 'Paste in a video link here'}),
            'description': forms.Textarea(  attrs = {
                                                'class': 'form-control',
                                                'row':2,
                                                'placeholder': 'Add a description'
                                                }),
            'notes': forms.Textarea(        attrs = {
                                                'class': 'form-control',
                                                'row':4,
                                                'placeholder': 'Add any notes'
                                                }),
                                                }
class VideoLectureSessionForm(forms.ModelForm):
    class Meta:
        model = VideoLectureSession
        fields =(
                "status",
                "completion_time",
                )
        widgets = {
            'status': forms.TextInput(attrs = {'type':'hidden'}),
            'completion_time': forms.NumberInput(attrs = {'type':'hidden',
                                                        "value":0}),

                }
