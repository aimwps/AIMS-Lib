from django.contrib import admin
from .models import Pathway, PathwayContent, PathwayParticipant

admin.site.register(Pathway)
admin.site.register(PathwayContent)
admin.site.register(PathwayParticipant)
