from django import forms
from .models import VideoLecture, WrittenLecture, Pathway, PathwayContentSetting, Quiz
from bootstrap_datepicker_plus import DatePickerInput



class BenchmarkNewForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('title',)
        widgets ={
            'title': forms.TextInput(attrs = {'class': 'form-control'}),
            }

class WrittenLectureEditForm(forms.ModelForm):
    class Meta:
        model = WrittenLecture
        fields = ('title',"body")
        widgets ={
            'title': forms.TextInput(attrs = {'class': 'form-control'}),
            'body': forms.Textarea(attrs = {'class': 'form-control',
                                            }),}

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
        user_quiz = sorted([(q.id, str(q)) for q in Quiz.objects.filter(author=user)])
        print(user_quiz)
        user_lit = sorted([(l.id, str(l)) for l in WrittenLecture.objects.filter(author=user)])
        print(user_lit)
        user_vid = sorted([(v.id, str(v)) for v in VideoLecture.objects.filter(author=user)])
        print(user_vid)
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

        # this is applying the css classes 'form-control' is predetermined
class WrittenLectureNewForm(forms.ModelForm):
    class Meta:
        model = WrittenLecture
        fields = ('title','body')
        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control'}),
            'body': forms.Textarea(attrs = {'class': 'form-control',}),
                }
