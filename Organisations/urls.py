from django.urls import path
from .views import (OrganisationView,
                    OrganisationCreate,
                    OrganisationEdit,
                    OrganisationContentView,
                    OrganisationContentCreate,
                    OrganisationContentEdit,
                    UserOrganisationsView,
                    getOrganisationData,
                    getOrganisationMembers,
                    searchExactUser,
                    submitNewMember,
                    getUserBookmarkedPathways,)
# from .views import

urlpatterns = [
    path('view-organisation/<int:organisation_id>/', OrganisationView.as_view(), name="organisation-view"),
    path('create-organisation/', OrganisationCreate.as_view(), name="organisation-create"),
    path('edit-organisation/<int:pk>/', OrganisationEdit.as_view(), name="organisation-edit"),
    path('view-organisation-content/<int:pk>', OrganisationContentView.as_view(), name="organisation-content-view"),
    path('create-organisation-content/<int:organisation_id>/', OrganisationContentCreate.as_view(), name="organisation-content-create"),
    path('edit-organisation-content/<int:organisation_id>/', OrganisationContentEdit.as_view(), name="organisation-content-edit"),
    path('my-organisations/', UserOrganisationsView.as_view(), name="user-organisations-view"),
    path("get_organisation_data/", getOrganisationData, name="get-org-data"),
    path("get_organisation_members/", getOrganisationMembers, name="get-org-members"),
    path("ajax_search_exact_user/", searchExactUser, name="search-exact-user"),
    path("ajax_submit_new_membership/", submitNewMember, name="submit-new-member"),
    path("ajax_get_user_and_bookmarked_pathway_data/", getUserBookmarkedPathways, name="get-user-pathway")
]
