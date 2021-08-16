from django import forms
from .models import Post, Comment, Reply


class ForumTopicNewForm(forms.ModelForm):
    class Meta:
        model= Post
        fields = ('title','dev_area', 'author', 'body', 'topic_snippet')
        widgets ={
            'title': forms.TextInput(attrs = {'class': 'form-control'}),
            'dev_area': forms.Select(attrs = {'class': 'form-control'}),
            'author': forms.TextInput(attrs = {'class': 'form-control', 'value': '', 'id':'user_input_ms', 'type': 'hidden'}),
            #'author': forms.Select(attrs = {'class': 'form-control'}),
            'body': forms.Textarea(attrs = {'class': 'form-control'}),
            'topic_snippet': forms.Textarea(attrs = {'class': 'form-control'}),}
        # this is applying the css classes 'form-control' is predetermined
        # as we are using bootstrap, can reference any css assigned

class ForumTopicNewCatForm(forms.ModelForm):
    class Meta:
        model= Post
        fields = ('title', 'body', 'topic_snippet')
        widgets ={
            'title': forms.TextInput(attrs = {
                                            'class': 'form-control',
                                            'placeholder': 'The title of your topic *'}),
            #'author': forms.Select(attrs = {'class': 'form-control'}),
            'body': forms.Textarea(attrs = {
                                            'class': 'form-control',
                                            'placeholder': 'The main body of your topic *'}),
            'topic_snippet': forms.Textarea(attrs = {
                                            'class': 'form-control',
                                            'placeholder': 'A brief description or preview of your topic',
                                            "rows": 6}),}


class ForumTopicEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title',"dev_area", 'body')
        widgets ={
            'title': forms.TextInput(attrs = {'class': 'form-control'}),
            'dev_area': forms.Select(attrs = {'class': 'form-control'}),
            'body': forms.Textarea(attrs = {'class': 'form-control',
                                            }),}
        # this is applying the css classes 'form-control' is predetermined
        # as we are using bootstrap, can reference any css assigned
class ForumTopicCommentForm(forms.Form):
    # content_author = forms.IntegerField(widget=forms.HiddenInput)
    # content_post = forms.IntegerField(widget=forms.HiddenInput)
    content_body = forms.CharField(max_length=500, label="", widget=forms.Textarea(attrs = {'class': 'form-control',
                                                                                            'rows':6, 'cols':100}))

class ForumTopicReplyForm(forms.ModelForm):
    def __init__( self, *args, **kwargs ):
        super(ForumTopicReplyForm, self).__init__( *args, **kwargs )
        self.fields['body'].label = "" #the trick :)
    class Meta:
        model = Reply
        fields = ('body',)
        widgets ={'body': forms.Textarea(attrs = {'class': 'form-control',})}
        # this is applying the css classes 'form-control' is predetermined
        # as we are using bootstrap, can reference any css assigned
