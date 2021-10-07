from django.contrib import admin
from .models import Behaviour, Aim, StepTracker, StepTrackerLog, StepTrackerCustomFrequency

admin.site.register(Behaviour)
admin.site.register(Aim)
admin.site.register(StepTracker)
admin.site.register(StepTrackerLog)
admin.site.register(StepTrackerCustomFrequency)
