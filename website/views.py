from django.shortcuts import render
from django.views.generic import TemplateView
def home(request):
    return render(request, 'home.html', {})

class LoginRegisterRequiredView(TemplateView):
    template_name = "login_register.html"



class AIMwpSView(TemplateView):
    template_name = "aimwps.html"
