from django.shortcuts import render, get_object_or_404
from .models import Organisation, OrganisationContent
from .forms import OrganisationCreateForm, OrganisationEditForm, OrganisationContentCreateForm, OrganisationContentEditForm
from Paths.models import Pathway
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView, View, ListView
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

def get_organisation_tree(organisation):
    children = organisation.children.all()
    if not children:
            return {"organisation": organisation, "suborganisation": []}
    else:
        return {"organisation": organisation, "suborganisation": [get_organisation_tree(child) for child in children]}


class OrganisationView(LoginRequiredMixin, View):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "organisation_view.html"
    def get(self, request, organisation_id):
        organisation = get_object_or_404(Organisation, id=organisation_id)
        organisation_tree = get_organisation_tree(organisation)


        if request.user.id == organisation.author.id:
            context = {"organisation_data": organisation_tree}
            print(context)

        else:
            context = {}
        return render(request, self.template_name, context)


class OrganisationCreate(LoginRequiredMixin, CreateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "organisation_create.html"
    model = Organisation
    form_class = OrganisationCreateForm
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('organisation-view', kwargs={'organisation_id' : self.object.pk})

class OrganisationEdit(LoginRequiredMixin, UpdateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "organisation_edit.html"
    model = Organisation
    form_class = OrganisationEditForm
    def get_success_url(self):
        return reverse('user-organisations-view')
################################################################################

class OrganisationContentView(LoginRequiredMixin, DetailView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "organisation_content_view.html"
    model = OrganisationContent


class OrganisationContentCreate(LoginRequiredMixin, View):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "organisation_content_create.html"
    def get(self, request, organisation_id):
        context = {
        "form_choices":sorted([(pathway.id, str(pathway.title)) for pathway in Pathway.objects.filter(author=self.request.user)]),
        "group_id": organisation_id}
        return render(request, self.template_name, context)
    def post(self, request, organisation_id):
        if "create_group_pathway" in request.POST:
            print(request.POST)
            new_group_pathway = OrganisationContent(
                            assigned_group = get_object_or_404(Organisation, id=organisation_id),
                            content_type = ContentType.objects.get_for_model(Pathway),
                            pathway = get_object_or_404(Pathway, id=request.POST.get('content_id')))


            new_group_pathway.save()
            return HttpResponseRedirect("/my-organisations/")



class OrganisationContentEdit(LoginRequiredMixin, UpdateView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "organisation_content_edit.html"
    model = OrganisationContent
    form_class = OrganisationContentEditForm
    def get(self, request, organisation_id):
        context = {
        "form": OrganisationContentCreateForm(user=request.user)}
        return render(request, self.template_name, context)

    def form_valid(self, form):
        form.instance.content_type = ContentType.objects.get_for_model(Pathway)
        return super().form_valid(form)


class UserOrganisationsView(LoginRequiredMixin,ListView):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "user_organisations.html"
    model = Organisation
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def get_queryset(self):
        x = Organisation.objects.filter(author=self.request.user)
        return x

    def post(self, request):

        if "delete_organisation" in request.POST:
            organisation = get_object_or_404(Organisation, id=request.POST.get("delete_organisation"))
            organisation.delete()
        else:
            print("fail")
        return HttpResponseRedirect("/my-organisations/")
