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
)

urlpatterns = [
    path('pathways/', PathsHomeView.as_view(), name="pathways"),
    path('create_pathway/', PathwayCreate.as_view(), name="pathway-create"),
    path('create_pathway_obj/<int:pathway_id>/', PathwayContentCreate.as_view(), name="pathway-content-create"),
    path('pathway/<int:pathway_id>/', PathwayView.as_view(), name="pathway-view"),
    path('pathway/develop/<int:pathway_id>/', PathwayDevelopView.as_view(), name="pathway-develop"),
    path('edit_pathway/<int:pk>/', PathwayEdit.as_view(), name="pathway-edit"),
    path('get_dev_pathway_content/', get_dev_pathway_content, name="pathway-dev-content-get"),
    path('dev_pathway_edit/', edit_dev_pathway_content, name="pathway-dev-content-edit")


]
