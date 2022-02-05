from django.shortcuts import render, get_object_or_404, redirect
from .models import Organisation, OrganisationContent, OrganisationMembers
from .forms import OrganisationCreateForm, OrganisationEditForm, OrganisationContentCreateForm, OrganisationContentEditForm
from Paths.models import Pathway, PathwayPurchase, PathwayCost
from Paths.pathway_serializers import PathwaySerializer, PathwayContentSerializer, PathwayCostSerializer
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView, View, ListView
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect,JsonResponse
from .organisation_serializers import OrganisationSerializer
from Members.members_serializers import UserSerializer
from django.contrib.auth.models import User
from django.db.models import Q
import json

def ajax_get_organisation_pathway_data(request):
    pathway = Pathway.objects.get(id=request.GET.get("pathway"))
    organisation = Organisation.objects.get(id=request.GET.get("organisation"))
    organisation_pathways = organisation.group_pathways.filter()
    organsation_member_ids = organisation.org_members.values_list("member_id")
    pathway_and_organisation_participants = pathway.participants.filter(author__in=organsation_member_ids)





    # Pathway participant


    pathway_data = PathwaySerializer(pathway)

    pathway_purchases = PathwayPurchase.objects.filter(purchase_type="organisation_paid", purchase_owner=organisation.find_root_organisation.id, status="active")





    data_info = {
                "branch_members": organisation.org_members.count() ,
                "active_members": pathway_and_organisation_participants.filter(purchase__status="spent").count() ,
                "pending_members": pathway_and_organisation_participants.filter(purchase__status="pending").count() ,
                "own_subscription_members": pathway_and_organisation_participants.filter(Q(purchase__status="spent"), Q(purchase__purchase_type="author_paid") | Q(purchase__purchase_type="author_free")).count() ,
                "pathway_available_invites": pathway_purchases.count() ,
                "pathway_costs": PathwayCostSerializer(pathway.cost_brackets.all().order_by("purchase_quantity"), many=True).data,
                "pathway": pathway_data.data,
                }

    return JsonResponse(data_info, safe=False)


def ajax_submit_organisation_invite(request):
    if request.method=="POST":
        invite = OrganisationMembers.objects.get(id=request.POST.get("invite_id"))

        invite.status = request.POST.get("status")
        invite.save()
        return JsonResponse({"success":"success"}, safe=False)
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
            if organisation.org_members.filter(member=request.user).exists() or organisation.author == request.user:
                organisation_tree = get_suborganisation_tree(organisation)
                organisation_list = get_suborganisation_list(organisation)
                parent_org_choices = [(organisation.id, organisation.title) for organisation in organisation_list]
                add_org_form = OrganisationCreateForm()
                add_org_form.fields['parent_organisation'].choices = parent_org_choices
                print(add_org_form)
                context = {"organisation_data": organisation_tree,
                            "root_organisation": organisation,
                            "organisation_list": organisation_list,
                            "admin_approved": False

                            }
                if request.user.id == organisation.author.id:
                    context["addOrganisationForm"]= add_org_form
                    context["admin_approved"] = True
                return render(request, self.template_name, context)
            else:
                return redirect("access-denied")
        else:
            root = organisation.find_root_organisation()
            return redirect("organisation", organisation_id=root.id)


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





        return redirect("organisation", organisation_id=organisation_id)

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
        print("yyyyyyyyyyyyyyyyyyyyyyyyy")
        print(self.object.pk)
        print("-----------------------------")
        return reverse('organisation', kwargs={'organisation_id' : self.object.pk})

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
        return Organisation.objects.filter(
                            (Q(parent_organisation=None) & Q(org_members__member=self.request.user)) |(Q(author=self.request.user) &Q(parent_organisation=None) )
                            ).distinct()


    def post(self, request):

        if "delete_organisation" in request.POST:
            organisation = get_object_or_404(Organisation, id=request.POST.get("delete_organisation"))
            organisation.delete()
        else:
            print("fail")
        return HttpResponseRedirect("/my-organisations/")
