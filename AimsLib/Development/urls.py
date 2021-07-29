from django.urls import path
from .views import AimView, AimsDash, AimNew, LeverNew, AssignTrackerView, LogTracker#, LogDash
# from .views import

urlpatterns = [
    path('anaim/', AimView.as_view(), name="an-aim"),
    path('aims_dash/', AimsDash.as_view(), name="aims-dash"),
    path('aims_new/', AimNew.as_view(), name="aims-new"),
    path('lever_new/<int:aim_id>/', LeverNew.as_view(), name="lever-new"),
    path('tracker_select/<int:lever_id>', AssignTrackerView.as_view(), name="tracker-select"),
    path('log_tracker/<int:tracker_id>', LogTracker.as_view(), name="log-tracker"),
    #path('logsdash/', LogDash.as_view(), name="logs-dash")
    #path('', views.home, name="home"),
]
