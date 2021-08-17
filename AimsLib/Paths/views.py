from django.shortcuts import render, get_object_or_404

from Members.models import MemberProfile
from django.views.generic import TemplateView, CreateView, View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

class PathsHomeView(TemplateView):
    template_name = "paths.html"
