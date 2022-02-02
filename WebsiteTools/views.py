from django.views.generic import TemplateView
from django.shortcuts import render
from Members.models import MemberProfile
from Paths.models import PathwayParticipant
from Organisations.organisation_serializers import OrganisationMembersSerializer
from Organisations.models import OrganisationMembers
from Paths.pathway_serializers import PathwayParticipantSerializer
from django.db.models import Q
from django.http import JsonResponse

def home(request):
    return render(request, 'home.html', {})

def nav_ajax_check_pathway_invites(request):
    if request.method == "GET":
        data = None
        if request.user.is_authenticated:
            pathway_invites = PathwayParticipant.objects.filter(Q(status="pending", author=request.user))
            data = PathwayParticipantSerializer(pathway_invites, many=True).data
        return JsonResponse(data, safe=False)

def nav_ajax_check_organisation_invites(request):
    if request.method =="GET":
        data = None
        if request.user.is_authenticated:
            organisation_invites = OrganisationMembers.objects.filter(Q(status="pending", member=request.user))
            data = OrganisationMembersSerializer(organisation_invites, many=True).data
        return JsonResponse(data, safe=False)


class LoginRegisterRequiredView(TemplateView):
    template_name = "login_register.html"

class AccessDeniedView(TemplateView):
    template_name = "access_denied.html"
