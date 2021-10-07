from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (PathsHomeView,
                    PathwayCreate,
                    PathwayContentCreate,
                    PathwayView,
                    PathwayDevelopView,
                    PathwayEdit,
)

urlpatterns = [
    path('pathways/', PathsHomeView.as_view(), name="pathways"),
    path('create_pathway/', PathwayCreate.as_view(), name="pathway-create"),
    path('create_pathway_obj/<int:pathway_id>/', PathwayContentCreate.as_view(), name="pathway-content-create"),
    path('pathway/<int:pk>/', PathwayView.as_view(), name="pathway-view"),
    path('pathway/develop/<int:pathway_id>/', PathwayDevelopView.as_view(), name="pathway-develop"),
    path('edit_pathway/<int:pk>/', PathwayEdit.as_view(), name="pathway-edit"),


]
