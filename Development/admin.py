from django.contrib import admin
from .models import SkillArea, DevelopmentCategory, Lever, Aim,TrackerMinAim, TrackerMinAimRecords, TrackerBoolean, TrackerBooleanRecords
admin.site.register(SkillArea)
admin.site.register(DevelopmentCategory)
admin.site.register(Lever)
admin.site.register(Aim)
admin.site.register(TrackerMinAim)
admin.site.register(TrackerMinAimRecords)
admin.site.register(TrackerBoolean)
admin.site.register(TrackerBooleanRecords)
