from django.urls import path
from .views import (OrganisationView,
                    OrganisationCreate,
                    OrganisationEdit,
                    OrganisationContentView,
                    OrganisationContentCreate,
                    OrganisationContentEdit,
                    UserOrganisationView)
# from .views import

urlpatterns = [
    path('view-organisation/<int:pk>/', OrganisationView.as_view(), name="view-organisation"),
    path('create-organisation/', OrganisationCreate.as_view(), name="create-organisation"),
    path('edit-organisation/<int:pk>/', OrganisationEdit.as_view(), name="edit-organisation"),
    path('view-organisation-content/<int:pk>', OrganisationContentView.as_view(), name="view-organisation-content"),
    path('create-organisation-content/<int:organisation_id>/', OrganisationContentCreate.as_view(), name="create-organisation-content"),
    path('edit-organisation-content/<int:organisation_id>/', OrganisationContentEdit.as_view(), name="edit-organisation-content"),
    path('my-organisations/', UserOrganisationsView.as_view(), name="view-user-organisations"),
]
