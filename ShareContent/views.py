from django.shortcuts import render, get_object_or_404
from .models import UserCreatedGroup, UserCreatedGroupContent
from .forms import UserGroupCreateForm, UserGroupEditForm, UserGroupPathwayCreateForm, UserGroupPathwayEditForm
from Paths.models import Pathway
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView
from django.contrib.contenttypes.models import ContentType
class UserGroupView(LoginRequiredMixin,DetailView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "user_group_view.html"
    model = UserCreatedGroup

class UserGroupCreate(LoginRequiredMixin, CreateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "user_group_create.html"
    model = UserCreatedGroup
    form_class = UserGroupCreateForm
    def form_valid(self, form):
        form.instance.founder= self.request.user
        return super().form_valid(form)

class UserGroupEdit(LoginRequiredMixin, UpdateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "user_group_edit.html"
    model = UserCreatedGroup
    form_class = UserGroupEditForm
    # def form_valid(self, form):
    #     form.instance.content_type = ContentType.objects.get_for_model(Pathway)
    #     return super().form_valid(form)
################################################################################

class UserGroupContentView(LoginRequiredMixin, DetailView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "user_group_content_view.html"
    model = UserCreatedGroupContent


class UserGroupPathwayCreate(LoginRequiredMixin, CreateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "user_group_content_create.html"
    model = UserCreatedGroupContent
    form_class = UserGroupPathwayCreateForm
    def form_valid(self, form):
        form.instance.assigned_group = get_object_or_404(UserCreatedGroup, id=self.kwargs['user_group_id'])
        form.instance.content_type = ContentType.objects.get_for_model(Pathway)
        return super().form_valid(form)

class UserGroupPathwayEdit(LoginRequiredMixin, UpdateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "user_group_content_edit.html"
    model = UserCreatedGroupContent
    form_class = UserGroupPathwayEditForm

    def form_valid(self, form):
        form.instance.content_type = ContentType.objects.get_for_model(Pathway)
        return super().form_valid(form)
