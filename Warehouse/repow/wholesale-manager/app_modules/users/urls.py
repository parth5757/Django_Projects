from django.urls import path
from app_modules.users.views import UserCreateView, UserDataTablesAjaxPagination, UserDeleteAjaxView, UserListView, UserUpdateView, ProfileUpdateView

app_name = "users"

urlpatterns = [
    # url for user
    path("", UserListView.as_view(), name="user_list"),
    path("create/", UserCreateView.as_view(), name="user_create"),
    path("<int:pk>/update/", UserUpdateView.as_view(), name="user_update"),
    path("user-delete-ajax/", UserDeleteAjaxView.as_view(), name="user_delete"),
    path('user-list-ajax/', UserDataTablesAjaxPagination.as_view(), name='user_list_ajax'),
    path("<int:pk>/profile/", ProfileUpdateView.as_view(), name="user_profile"),
]

    