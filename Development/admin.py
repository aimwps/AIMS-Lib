from django.contrib import admin
from .models import Behaviour, Aim, StepTracker, StepTrackerLogs

admin.site.register(Behaviour)
admin.site.register(Aim)
admin.site.register(StepTracker)
admin.site.register(StepTrackerLogs)
