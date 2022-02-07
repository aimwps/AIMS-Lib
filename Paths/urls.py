from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (PathsHomeView,
                    PathwayCreate,
                    PathwayContentCreate,
                    PathwayView,
                    PathwayDevelopView,
                    PathwayEdit,
                    get_dev_pathway_content,
                    edit_dev_pathway_content,
                    get_pathway_content_obj,
                    submit_content_setting_changes,
                    submit_cotent_delete,
                    UserPathways_ajax_get_pathway_costs,
                    UserPathways_ajax_check_pathway_invites,
                    UserPathways_ajax_submit_pathway_invite,
)

urlpatterns = [
    path('pathways/user', PathsHomeView.as_view(), name="pathways"),
    path('pathway/create', PathwayCreate.as_view(), name="pathway-create"),
    path('pathway/add_content/<int:pathway_id>/', PathwayContentCreate.as_view(), name="pathway-content-create"),
    path('pathway/<int:pathway_id>/', PathwayView.as_view(), name="pathway-view"),
    path('pathway/develop/<int:pathway_id>/', PathwayDevelopView.as_view(), name="pathway-develop"),
    path('pathway/update/<int:pk>/', PathwayEdit.as_view(), name="pathway-edit"),
    path('get_dev_pathway_content/', get_dev_pathway_content, name="pathway-dev-content-get"),
    path('dev_pathway_edit/', edit_dev_pathway_content, name="pathway-dev-content-edit"),
    path('ajax_get_pathway_content_obj/', get_pathway_content_obj, name="pathway-dev-content-modal-edit"),
    path('ajax_submit_content_setting_changes/', submit_content_setting_changes, name="content-setting-changes-submit"),
    path('ajax_submit_delete_pathway_content/', submit_cotent_delete, name="submit-content-delete"),
    path("UserPathways_ajax_get_pathway_costs/", UserPathways_ajax_get_pathway_costs, name="get-pathway-costs"),
    path("UserPathways_ajax_check_pathway_invites/", UserPathways_ajax_check_pathway_invites, name="check-pathway-invites"),
    path("UserPathways_ajax_submit_pathway_invite/", UserPathways_ajax_submit_pathway_invite, name="submit-pathway-invite"),


]
