from django.urls import path
from .views import AimView, AimsDash, AimCreate, BehaviourCreate, BehaviourEdit, AimEdit
# from .views import

urlpatterns = [
    path('aim/view/', AimView.as_view(), name="an-aim"),
    path('aims/', AimsDash.as_view(), name="aims-dash"),
    path('aim/create/', AimCreate.as_view(), name="aim-create"),
    path('behaviour/create/<int:aim_id>/', BehaviourCreate.as_view(), name="behaviour-create"),
    path('behaviour/edit/<int:pk>', BehaviourEdit.as_view(), name="behaviour-edit"),
    path('aim/edit/<int:pk>', AimEdit.as_view(), name="aim-edit")

]
