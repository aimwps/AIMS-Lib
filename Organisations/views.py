from django.shortcuts import render, get_object_or_404, redirect
from .models import Organisation, OrganisationContent, OrganisationMembers
from .forms import OrganisationCreateForm, OrganisationEditForm, OrganisationContentCreateForm, OrganisationContentEditForm
from Paths.models import Pathway
from Paths.pathway_serializers import PathwaySerializer
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView, View, ListView
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect,JsonResponse
from .organisation_serializers import OrganisationSerializer
from Members.members_serializers import UserSerializer
from django.contrib.auth.models import User
import json

def getUserBookmarkedPathways(request):
    if request.method=="GET":
        user_pathways = Pathway.objects.filter(author=request.user)
        data_info = {"created": None,
                    "user_bookmarked": None,
                    "organisation_bookmarked": None}

        if user_pathways:
            data_info['created'] = PathwaySerializer(user_pathways, many=True).data
        return JsonResponse(data_info, safe=False)

def submitNewMember(request):
    if request.method=="POST":
        print(request.POST)
        user = get_object_or_404(User, id=request.POST.get("user_id"))
        organisation = get_object_or_404(Organisation, id=request.POST.get("organisation_id"))
        new_membership = OrganisationMembers(organisation=organisation, member=user, status="pending")
        new_membership.save()
        data_info = {"message": "Success"}
        json_data_info = json.dumps(data_info)
        return JsonResponse(json_data_info, safe=False)

def searchExactUser(request):
    if request.method=="GET":
        print(request.GET)
        search_phrase = request.GET.get("search_phrase")
        user = User.objects.filter(email__iexact=search_phrase) | User.objects.filter(username__iexact=search_phrase)
        if user:
            user=user[0]
            user_data = UserSerializer(user)
            user_data_complete = {
                                "status" : None,
                                "user" : user_data.data
                                }
            selected_organisation_id = request.GET.get("selected_organisation")
            selected_organisation = Organisation.objects.get(id=selected_organisation_id)
            root_organisation = selected_organisation.find_root_organisation()

            # for the found user, check there status in the selected organisation and
            # the rooot organisation
            # selected_organisation_member = OrganisationMembers.objects.filter(organisation=selected_organisation,
            #                                                                 member=user)
            root_organisation_member = OrganisationMembers.objects.filter(organisation=root_organisation,
                                                                        member=user)
            root_organisation_data = OrganisationSerializer(root_organisation)

            if root_organisation_member:
                user_data_complete['status'] = {"organisation":root_organisation_data.data, "status":root_organisation_member[0].status}
            else:
                user_data_complete['status'] = {"organisation":root_organisation_data.data, "status": "no membership"}


            return JsonResponse(user_data_complete, safe=False)



        else:
            return JsonResponse(json.dumps({
                                "status": None,
                                "user": None
                                }), safe=False)

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
        if organisation.is_root():
            organisation_tree = get_suborganisation_tree(organisation)
            organisation_list = get_suborganisation_list(organisation)
            parent_org_choices = [(organisation.id, organisation.title) for organisation in organisation_list]
            add_org_form = OrganisationCreateForm()
            add_org_form.fields['parent_organisation'].choices = parent_org_choices

            if request.user.id == organisation.author.id:
                context = {"organisation_data": organisation_tree,
                            "root_organisation": organisation,
                            "organisation_list": organisation_list,
                            "addOrganisationForm": add_org_form,

                            }
            else:
                context = {}
            return render(request, self.template_name, context)
        else:
            root = organisation.find_root_organisation()
            return redirect("organisation-view", organisation_id=root.id)


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

        if "add_pathways_to_organisation" in request.POST:
            new_pathway_ids = request.POST.getlist("addPathways")
            organisation = Organisation.objects.get(id=request.POST.get("add_pathways_to_organisation"))
            for new_pathway_id in new_pathway_ids:
                organisation_content = OrganisationContent.objects.filter(assigned_group=organisation, pathway=new_pathway_id)
                if not organisation_content:
                    pathway = Pathway.objects.get(id=new_pathway_id)
                    new_content_for_organisation = OrganisationContent(assigned_group=organisation, content_type="pathway", pathway=pathway)
                    new_content_for_organisation.save()





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
