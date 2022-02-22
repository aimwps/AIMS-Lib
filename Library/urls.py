from django.urls import path
from .views import (LibraryView,
                    LibraryView_ajax_search_library,
                    LibraryView_ajax_get_library_result,
                    LibraryView_ajax_use_content,
                    LibraryView_ajax_get_user_bookmarks,
                    LibraryView_ajax_get_bookmark_content,
                    ajax_get_library_permissions,
                    ajax_edit_library_permissions
                    )

urlpatterns = [
    path("library/", LibraryView.as_view(), name="library"),
    path("LibraryView_ajax_search_library/",  LibraryView_ajax_search_library, name="library-search"),
    path("LibraryView_ajax_get_library_result/", LibraryView_ajax_get_library_result, name="library-result"),
    path("LibraryView_ajax_use_content/", LibraryView_ajax_use_content, name="library-use-content"),
    path("LibraryView_ajax_get_user_bookmarks/", LibraryView_ajax_get_user_bookmarks, name="library-get-bookmarks"),
    path("LibraryView_ajax_get_bookmark_content/", LibraryView_ajax_get_bookmark_content, name="library-load-bookmark"),
    path("ajax_get_library_permissions/", ajax_get_library_permissions, name="get-library-permissions"),
    path("ajax_edit_library_permissions/", ajax_edit_library_permissions, name="edit-library-permissions"),



]
