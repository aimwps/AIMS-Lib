from django.shortcuts import render, get_object_or_404, redirect
from .models import Organisation, OrganisationContent, OrganisationMembers
from .forms import OrganisationCreateForm, OrganisationEditForm, OrganisationContentCreateForm, OrganisationContentEditForm
from Paths.models import Pathway
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView, View, ListView
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect,JsonResponse
from .organisation_serializers import OrganisationSerializer
from Members.members_serializers import UserSerializer
from django.contrib.auth.models import User
import json


def getOrganisationMembers(request):
    if request.method =="GET":
        organisation = get_object_or_404(Organisation, id=request.GET.get("organisation_id"))
        members = OrganisationMembers.objects.filter(organisation=organisation)
        member_ids = members.values_list('member', flat=True)
        members_only = User.objects.filter(pk__in=member_ids)
        serialize = UserSerializer(members_only, many=True)

    return JsonResponse(serialize.data, safe=False)

def getOrganisationData(request):

    if request.method == "GET":
        organisation = get_object_or_404(Organisation, id=request.GET.get("organisation_id"))
        serialize = OrganisationSerializer(organisation)

    return JsonResponse(serialize.data, safe=False)

def get_suborganisation_tree(organisation):
    #  Find all the childrenn of the oganisation
    children = organisation.children.all()
    # If there are no children
    if not children:
            return {}
    else:
    # for each of their children repeat the process until all children are found
        return {child: get_suborganisation_tree(child) for child in children}

def get_suborganisation_list(organisation, organisation_list=[]):
    if not organisation_list:
        organisation_list = [organisation]
    for child in organisation.children.all():
        organisation_list.append(child)
        get_suborganisation_list(organisation=child, organisation_list=organisation_list)
    return organisation_list




class OrganisationView(LoginRequiredMixin, View):
    login_url = '/login-or-register/'
    redirect_field_name = 'redirect_to'
    template_name = "organisation_view.html"
    def get(self, request, organisation_id):
        organisation = get_object_or_404(Organisation, id=organisation_id)
        organisation_tree = get_suborganisation_tree(organisation)
        organisation_list = get_suborganisation_list(organisation)
        parent_org_choices = [(organisation.id, organisation.title) for organisation in organisation_list]
        add_org_form = OrganisationCreateForm()
        add_org_form.fields['parent_organisation'].choices = parent_org_choices

        if request.user.id == organisation.author.id:
            context = {"organisation_data": organisation_tree,
                        "root_organisation": organisation,
                        "addOrganisationForm": add_org_form,

                        }
        else:
            context = {}
        return render(request, self.template_name, context)



    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def post(self, request, organisation_id):
        print(request.POST)
        if "create_sub_organisation" in request.POST:
            new_organisation = Organisation(
                                author=request.user,
                                title=request.POST.get("title"),
                                parent_organisation = Organisation.objects.get(id=request.POST.get("parent_organisation")),
                                )
            new_organisation.save()
            new_members = User.objects.filter(pk__in=request.POST.getlist("members"))
            for user in new_members:
                new_member = OrganisationMembers(organisation=new_organisation, member=user, status="pending")
                new_member.save()

        if "add_members_to_org_by_id" in request.POST:

            new_members = User.objects.filter(pk__in=request.POST.getlist("updatemembers"))
            for user in new_members:
                new_member = OrganisationMembers(
                                    organisation = Organisation.objects.get(id=request.POST.get("add_members_to_org_by_id")),
                                    member=user,
                                    status="active")

                new_member.save()


        return redirect("organisation-view", organisation_id=organisation_id)

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
