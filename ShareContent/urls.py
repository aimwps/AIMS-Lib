from django.urls import path
from .views import (UserGroupView,
                    UserGroupCreate,
                    UserGroupEdit,
                    UserGroupContentView,
                    UserGroupPathwayCreate,
                    UserGroupPathwayEdit,)
# from .views import

urlpatterns = [
    path('view-group/', UserGroupView.as_view(), name="view-user-group"),
    path('new-group/', UserGroupCreate.as_view(), name="create-user-group"),
    path('edit-group/', UserGroupEdit.as_view(), name="edit-user-group"),
    path('view-group-content/', UserGroupContentView.as_view(), name="view-group-content"),
    path('new-group-content/', UserGroupPathwayCreate.as_view(), name="create-group-pathway-content"),
    path('edit-group-content/', UserGroupPathwayEdit.as_view(), name="edit-group-pathway-content"),
]
