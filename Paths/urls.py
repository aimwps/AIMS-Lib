from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (PathsHomeView,
                    PathwayNew,
                    PathwayObjNew,
                    PathwayView,
                    EditPathwayView,
)

urlpatterns = [
    path('pathway/', PathsHomeView.as_view(), name="skill-paths"),
    path('create_pathway/', PathwayNew.as_view(), name="new-pathway"),
    path('create_pathway_obj/<int:pathway_id>/', PathwayObjNew.as_view(), name="new-pathway-obj"),
    path('pathway/<int:pathway_id>', PathwayView.as_view(), name="view-pathway"),
    path('edit_pathway/<int:pk>/', EditPathwayView.as_view(), name="edit-pathway"),




]
