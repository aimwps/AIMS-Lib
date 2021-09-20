from django import forms
from .models import Pathway, PathwayContentSetting
from bootstrap_datepicker_plus import DatePickerInput
from Benchmark.models import Quiz
from VideoLecture.models import VideoLecture
from WrittenLecture.models import WrittenLecture


class PathwayEditForm(forms.ModelForm):
    class Meta:
        model = Pathway
        fields = ('title',"description")
        widgets ={
            'title': forms.TextInput(attrs = {'class': 'form-control'}),
            'description': forms.Textarea(attrs = {'class': 'form-control',
                                            }),}

class PathwayObjNewForm(forms.ModelForm):
    class Meta:
        model =  PathwayContentSetting
        fields = ('video_lecture', 'written_lecture', 'quiz','must_revise_continous', 'must_complete_previous')
        widgets = {'video_lecture': forms.Select(attrs={'class': 'form-control'}),
                    'written_lecture': forms.Select(attrs={'class': 'form-control'}),
                    'quiz': forms.Select(attrs={'class': 'form-control'}),
                    'must_revise_continous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                    'must_complete_previous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    def __init__(self, user=None, *args,**kwargs):
        super(PathwayObjNewForm, self).__init__(*args, **kwargs)
        user_quiz = sorted([(q.id, str(q.title)) for q in Quiz.objects.filter(author=user)])
        user_lit = sorted([(l.id, str(l.title)) for l in WrittenLecture.objects.filter(author=user)])
        user_vid = sorted([(v.id, str(v.title)) for v in VideoLecture.objects.filter(author=user)])
        self.fields['quiz'].choices = user_quiz
        self.fields['written_lecture'].choices = user_lit
        self.fields['video_lecture'].choices = user_vid

class PathwayNewForm(forms.ModelForm):
    class Meta:
        model =  Pathway
        fields = ('title', 'description')
        widgets ={
            'title': forms.TextInput(attrs = {'class': 'form-control',
                                            'placeholder': 'The title of your pathway'}),
            'description': forms.Textarea(attrs = {'class': 'form-control',
                                                    'placeholder': 'A description of your pathway'}),}
