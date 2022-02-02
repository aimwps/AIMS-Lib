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
                    getUserBookmarkedPathways,
                    ajax_submit_organisation_invite,)
# from .views import

urlpatterns = [
    path('organisation/<int:organisation_id>/', OrganisationView.as_view(), name="organisation"),
    path('organisation/create', OrganisationCreate.as_view(), name="create-organisation"),
    path('organisation/edit/<int:pk>/', OrganisationEdit.as_view(), name="update-organisation"),
    path('organisation/content/<int:pk>', OrganisationContentView.as_view(), name="organisation-content-view"),
    path('organisation/create/<int:organisation_id>/', OrganisationContentCreate.as_view(), name="organisation-content-create"),
    path('edit-organisation-content/<int:organisation_id>/', OrganisationContentEdit.as_view(), name="organisation-content-edit"),
    path('organisations/', UserOrganisationsView.as_view(), name="user-organisations-view"),
    path("get_organisation_data/", getOrganisationData, name="get-org-data"),
    path("get_organisation_members/", getOrganisationMembers, name="get-org-members"),
    path("ajax_search_exact_user/", searchExactUser, name="search-exact-user"),
    path("ajax_submit_new_membership/", submitNewMember, name="submit-new-member"),
    path("ajax_get_user_and_bookmarked_pathway_data/", getUserBookmarkedPathways, name="get-user-pathway"),
    path("ajax_submit_organisation_invite/", ajax_submit_organisation_invite, name="submit-org-invite"),
]
