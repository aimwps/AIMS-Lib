from django import forms
from .models import Article


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
