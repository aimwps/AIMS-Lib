from django.contrib import admin
from .models import Pathway, PathwayContent, PathwayParticipant, PathwayPurchase, PathwayCost

admin.site.register(Pathway)
admin.site.register(PathwayContent)
admin.site.register(PathwayParticipant)
admin.site.register(PathwayCost)
admin.site.register(PathwayPurchase)
