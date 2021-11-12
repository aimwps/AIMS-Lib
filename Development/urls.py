from django.urls import path
from .views import AimView, AimsDash, AimCreate, BehaviourCreate, BehaviourEdit, AimEdit, StepTrackerCreate, request_uncomplete_trackers,submit_tracker_log, get_tracker_calmap_data
# from .views import

urlpatterns = [
    path('aim/view/', AimView.as_view(), name="an-aim"),
    path('aims/', AimsDash.as_view(), name="aims-dash"),
    path('aim/create/', AimCreate.as_view(), name="aim-create"),
    path('behaviour/create/<int:aim_id>/', BehaviourCreate.as_view(), name="behaviour-create"),
    path('behaviour/edit/<int:pk>', BehaviourEdit.as_view(), name="behaviour-edit"),
    path('aim/edit/<int:pk>', AimEdit.as_view(), name="aim-edit"),
    path('steptracker/create/<int:behaviour_id>', StepTrackerCreate.as_view(), name="steptracker-create"),
    path('get_quickfire_trackers/', request_uncomplete_trackers, name="get-quickfire-trackers"),
    path('submit_tracker/', submit_tracker_log, name="submit-tracker_log"),
    path('get_calmap_data/', get_tracker_calmap_data, name="get-heatmap-data"),



]
