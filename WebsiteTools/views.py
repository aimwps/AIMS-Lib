from django.views.generic import TemplateView
from django.shortcuts import render
from Members.models import MemberProfile
def home(request):
    return render(request, 'home.html', {})

class LoginRegisterRequiredView(TemplateView):
    template_name = "login_register.html"
