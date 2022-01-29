from django import forms
from .models import Article, ArticleSession


class ArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title',"body")
        widgets ={
            'title': forms.TextInput(attrs = {'class': 'form-conrtrol text-center',
                                            "placeholder": "Insert an article title here"}),
            'body': forms.Textarea(attrs = {'class': 'form-control',
                                            }),}

        # this is applying the css classes 'form-control' is predetermined
class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title','body')
        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control text-center',
                                            "placeholder": "Insert an article title here"}),
            'body': forms.Textarea(attrs = {'class': 'form-control',}),
                }

class ArticleSessionForm(forms.ModelForm):
    class Meta:
        model = ArticleSession
        fields =(
                "status",
                "completion_time",
                )
        widgets = {
            'status': forms.TextInput(attrs = {'type':'hidden'}),
            'completion_time': forms.NumberInput(attrs = {'type':'hidden',
                                                        "value":0}),

                }
