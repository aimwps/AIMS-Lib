from django.urls import path
from .views import (LibraryView,
                    LibraryView_ajax_search_library,
                    LibraryView_ajax_get_library_result,
                    )

urlpatterns = [
    path("LibraryView_ajax_search_library/",  LibraryView_ajax_search_library, name="library-search"),
    path("library/", LibraryView.as_view(), name="library"),
    path("LibraryView_ajax_get_library_result/", LibraryView_ajax_get_library_result, name="library-result")

]
