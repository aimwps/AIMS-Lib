from django.urls import path
from .views import AimView, AimsDash, AimNew, LeverNew, TrackerSelect, TrackerMinAimNew
# from .views import

urlpatterns = [
    path('anaim/', AimView.as_view(), name="an-aim"),
    path('aims_dash/', AimsDash.as_view(), name="aims-dash"),
    path('aims_new/', AimNew.as_view(), name="aims-new"),
    path('lever_new/<int:aim_id>/', LeverNew.as_view(), name="lever-new"),
    path('tracker_select/<int:lever_id>', TrackerSelect.as_view(), name="tracker-select"),
    path('tracker_min_aim/<int:lever_id>', TrackerMinAimNew.as_view(), name="tracker-min-aim"),
    #path('', views.home, name="home"),
]
