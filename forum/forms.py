from django import forms
from .models import Post, Comment, Reply


class TopicCreateForm(forms.ModelForm):
    class Meta:
        model= Post
        fields = ('title','dev_area', 'author', 'body', 'topic_snippet')
        widgets ={
            'title': forms.TextInput(attrs = {'class': 'form-control'}),
            'dev_area': forms.Select(attrs = {'class': 'form-control'}),
            'author': forms.TextInput(attrs = {'class': 'form-control', 'value': '', 'id':'user_input_ms', 'type': 'hidden'}),
            'body': forms.Textarea(attrs = {'class': 'form-control'}),
            'topic_snippet': forms.Textarea(attrs = {'class': 'form-control'}),}


class TopicCreateInCatForm(forms.ModelForm):
    class Meta:
        model= Post
        fields = ('title', 'body', 'topic_snippet')
        widgets ={
            'title': forms.TextInput(attrs = {
                                            'class': 'form-control',
                                            'placeholder': 'The title of your topic *'}),
            'body': forms.Textarea(attrs = {
                                            'class': 'form-control',
                                            'placeholder': 'The main body of your topic *'}),
            'topic_snippet': forms.Textarea(attrs = {
                                            'class': 'form-control',
                                            'placeholder': 'A brief description or preview of your topic',
                                            "rows": 6}),}

class TopicEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title',"dev_area", 'body')
        widgets ={
            'title': forms.TextInput(attrs = {'class': 'form-control'}),
            'dev_area': forms.Select(attrs = {'class': 'form-control'}),
            'body': forms.Textarea(attrs = {'class': 'form-control',
                                            }),}

class TopicCommentForm(forms.Form):

    content_body = forms.CharField(max_length=500, label="", widget=forms.Textarea(attrs = {'class': 'form-control',
                                                                                            'rows':6, 'cols':100}))

class ReplyCreateForm(forms.ModelForm):
    def __init__( self, *args, **kwargs ):
        super(ForumTopicReplyForm, self).__init__( *args, **kwargs )
    class Meta:
        model = Reply
        fields = ('body',)
        widgets ={'body': forms.Textarea(attrs = {'class': 'form-control',})}
