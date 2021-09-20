from django.shortcuts import render, get_object_or_404
from .models import UserCreatedGroup, UserCreatedGroupContent
from .forms import UserGroupCreateForm, UserGroupEditForm, UserGroupPathwayCreateForm, UserGroupPathwayEditForm
from Paths.models import Pathway
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView, View
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
    def get_success_url(self):
        return reverse('view-user-group', kwargs={'pk' : self.object.pk})

class UserGroupEdit(LoginRequiredMixin, UpdateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "user_group_edit.html"
    model = UserCreatedGroup
    form_class = UserGroupEditForm
    def get_success_url(self):
        return reverse('view-user-group', kwargs={'pk' : self.object.pk})
################################################################################

class UserGroupContentView(LoginRequiredMixin, DetailView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "user_group_content_view.html"
    model = UserCreatedGroupContent


class UserGroupPathwayCreate(LoginRequiredMixin, View):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "user_group_content_create.html"
    def get(self, request, user_group_id):
        context = {
        "form_choices":sorted([(pathway.id, str(pathway.title)) for pathway in Pathway.objects.filter(author=self.request.user)]),
        "group_id": user_group_id}
        return render(request, self.template_name, context)
    def post(self, request, user_group_id):
        if "create_group_pathway" in request.POST:
            print(request.POST)
            new_group_pathway = UserCreatedGroupContent(
                            assigned_group = get_object_or_404(UserCreatedGroup, id=user_group_id),
                            content_type=ContentType.objects.get_for_model(Pathway),
                            content_id= request.POST.get('content_id'))


            new_group_pathway.save()
            return reverse("view-user-group", kwargs={"pk":user_group_id})



class UserGroupPathwayEdit(LoginRequiredMixin, UpdateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "user_group_content_edit.html"
    model = UserCreatedGroupContent
    form_class = UserGroupPathwayEditForm
    def get(self, request, user_group_id):
        context = {
        "form": UserGroupPathwayCreateForm(user=request.user)}
        return render(request, self.template_name, context)

    def form_valid(self, form):
        form.instance.content_type = ContentType.objects.get_for_model(Pathway)
        return super().form_valid(form)
