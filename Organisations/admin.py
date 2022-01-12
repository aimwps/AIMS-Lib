from django.contrib import admin
from .models import Organisation, OrganisationContent, OrganisationMembers

admin.site.register(Organisation)
admin.site.register(OrganisationContent)
admin.site.register(OrganisationMembers)
