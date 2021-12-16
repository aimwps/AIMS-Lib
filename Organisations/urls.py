from django.urls import path
from .views import (OrganisationView,
                    OrganisationCreate,
                    OrganisationEdit,
                    OrganisationContentView,
                    OrganisationContentCreate,
                    OrganisationContentEdit,
                    UserOrganisationsView)
# from .views import

urlpatterns = [
    path('view-organisation/<int:organisation_id>/', OrganisationView.as_view(), name="organisation-view"),
    path('create-organisation/', OrganisationCreate.as_view(), name="organisation-create"),
    path('edit-organisation/<int:pk>/', OrganisationEdit.as_view(), name="organisation-edit"),
    path('view-organisation-content/<int:pk>', OrganisationContentView.as_view(), name="organisation-content-view"),
    path('create-organisation-content/<int:organisation_id>/', OrganisationContentCreate.as_view(), name="organisation-content-create"),
    path('edit-organisation-content/<int:organisation_id>/', OrganisationContentEdit.as_view(), name="organisation-content-edit"),
    path('my-organisations/', UserOrganisationsView.as_view(), name="user-organisations-view"),
]
