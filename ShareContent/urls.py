from django.urls import path
from .views import (UserGroupView,
                    UserGroupCreate,
                    UserGroupEdit,
                    UserGroupContentView,
                    UserGroupPathwayCreate,
                    UserGroupPathwayEdit,
                    AllMyUserGroupsView)
# from .views import

urlpatterns = [
    path('view-group/<int:pk>/', UserGroupView.as_view(), name="view-user-group"),
    path('new-group/', UserGroupCreate.as_view(), name="create-user-group"),
    path('edit-group/<int:pk>/', UserGroupEdit.as_view(), name="edit-user-group"),
    path('view-group-content/<int:pk>', UserGroupContentView.as_view(), name="view-group-content"),
    path('new-group-pathway/<int:user_group_id>/', UserGroupPathwayCreate.as_view(), name="create-group-pathway-content"),
    path('edit-group-pathway/<int:user_group_id>/', UserGroupPathwayEdit.as_view(), name="edit-group-pathway-content"),
    path('my-groups/', AllMyUserGroupsView.as_view(), name="view-my-groups"),
]
