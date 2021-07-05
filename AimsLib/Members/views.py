from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.urls import reverse_lazy
from .forms import MemberRegisterForm, MemberEditForm, MemberEditPasswordForm
from django.contrib.auth.views import PasswordChangeView
from .models import MemberProfile

# Create your views here.

class MemberRegisterView(generic.CreateView):
    form_class = MemberRegisterForm
    template_name ="registration/member_register.html"
    success_url = reverse_lazy('login')

class MemberEditView(generic.UpdateView):
    form_class = MemberEditForm
    template_name ="registration/member_edit.html"
    success_url = reverse_lazy('home')
    def get_object(self):
        return self.request.user

class MemberEditPasswordView(PasswordChangeView):
    form_class = MemberEditPasswordForm
    success_url = reverse_lazy('home')
    template_name='registration/change_password.html'
    #template_name

class MemberProfileView(generic.DetailView):
    model = MemberProfile
    template_name = "member_profile.html"

    def get_context_data(self,*args, **kwargs):
        #users = MemberProfile.objects.all()
        context = super(MemberProfileView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(MemberProfile, id=self.kwargs['pk'])
        context['page_user'] = page_user

        return context
