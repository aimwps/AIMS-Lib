from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import MemberProfile
from django import forms

class MemberProfileForm(forms.ModelForm):
    class Meta:
        model= MemberProfile
        fields = ('power_quote', 'biography', 'personal_website', 'week_reset_day', 'month_reset_day', 'year_reset_month')
        widgets ={
            'power_quote': forms.Textarea(attrs = {
                                            'class': 'form-control',
                                            'placeholder': "Something that inspires you",
                                            "rows": 3}),
            'biography': forms.Textarea(attrs = {
                                            'class': 'form-control',
                                            'placeholder': "A little bit about yourself",
                                            "rows": 3}),
            'personal_website': forms.Textarea(attrs = {
                                            'class': 'form-control',
                                            'placeholder': 'a link to your own website',
                                            "rows":1,
                                            }),
            'week_reset_day': forms.Select(attrs = {
                                            'class': 'form-control',
                                            }),
            'month_reset_day': forms.TextInput(attrs = {
                                            'class': 'form-control',
                                            }),
            'year_reset_month': forms.TextInput(attrs = {
                                            'class': 'form-control',
                                            }),

                                            }

class MemberRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name =forms.CharField(max_length=100, widget=forms.TextInput(attrs = {'class': 'form-control'}))
    last_name =forms.CharField(max_length=100, widget=forms.TextInput(attrs = {'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    def __init__(self, *args,**kwargs):
        super(MemberRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class MemberEditForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs = {'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs = {'class': 'form-control'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs = {'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class MemberEditPasswordForm(PasswordChangeForm):
    old_password= forms.CharField(max_length=100, widget=forms.PasswordInput(attrs = {'class': 'form-control', "type":'password'}))
    new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs = {'class': 'form-control', "type":'password'}))
    new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs = {'class': 'form-control', "type":'password'}))
    class Meta:
        model = User
        fields = ('old_password','new_password1', 'new_password1')
