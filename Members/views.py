from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .forms import MemberProfileForm
from django.urls import reverse_lazy, reverse
from .forms import MemberRegisterForm, MemberEditForm, MemberEditPasswordForm
from django.contrib.auth.views import PasswordChangeView
from .models import MemberProfile
from django.contrib.auth.mixins import LoginRequiredMixin


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
        user_profile = get_object_or_404(MemberProfile, id=self.kwargs['pk'])
        context['user_profile'] = user_profile

        return context


class MemberProfileCreate(LoginRequiredMixin, generic.CreateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model = MemberProfile
    form_class = MemberProfileForm
    template_name ="registration/create_profile.html"
    success_url = reverse_lazy('aims-dash')

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class MemberProfileEdit(LoginRequiredMixin, generic.UpdateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    model = MemberProfile
    form_class = MemberProfileForm
    template_name ="registration/edit_profile.html"

    def get_success_url(self):
        return reverse('member-profile', kwargs={"pk": self.request.user.profile.id})
    def get_context_data(self,*args, **kwargs):
        #users = MemberProfile.objects.all()
        context = super(MemberProfileEdit, self).get_context_data(*args, **kwargs)
        user_profile = get_object_or_404(MemberProfile, author=self.kwargs['pk'])
        context['user_profile'] = user_profile
        return context
    def form_valid(self,form):
        form.instance.user_profile = self.request.user
        return super().form_valid(form)
