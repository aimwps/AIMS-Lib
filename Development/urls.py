from django.urls import path
from .views import AimView, AimsDash, AimNew, LeverNew, AssignTrackerView, LogAnyTracker, TrackerMinAimEdit, TrackerBooleanEdit, LeverEdit, AimEdit
# from .views import

urlpatterns = [
    path('anaim/', AimView.as_view(), name="an-aim"),
    path('aims_dash/', AimsDash.as_view(), name="aims-dash"),
    path('aims_new/', AimNew.as_view(), name="aims-new"),
    path('lever_new/<int:aim_id>/', LeverNew.as_view(), name="lever-new"),
    path('tracker_select/<int:lever_id>', AssignTrackerView.as_view(), name="tracker-select"),
    path('log_tracker/<str:tracker_type>/<int:tracker_id>', LogAnyTracker.as_view(), name="log-any-tracker"),
    path('edit_tracker/minaim/<int:pk>', TrackerMinAimEdit.as_view(), name="edit-min-tracker"),
    path('edit_tracker/yesno/<int:pk>', TrackerBooleanEdit.as_view(), name="edit-bool-tracker"),
    path('edit_behaviour/<int:pk>', LeverEdit.as_view(), name="edit-lever"),
    path('edit_aim/<int:pk>', AimEdit.as_view(), name="edit-aim")

]
