"""
URL configuration for app.
"""
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from app.views import *

router = DefaultRouter()
router.register('create_student', CreateStudentView, basename="create_student")
router.register('hello', HelloViewSet, basename="hello")
router.register('users', UserViewSet, basename="users")

urlpatterns = [
    
    path('', include(router.urls)),

    path('hello_drf/', hello_drf, name="hello_drf"),
    path('hello_world/', hello_world, name="hello_world"),
    path('hello_jwt/', HelloJWTView.as_view(), name="hello_jwt"),

    path('tasks/', TaskGenericView.as_view(), name="task_generic_todo"),
    path('tasks/<int:task_id>/', TaskDetailGenericView.as_view(), name="task_detail_generic_todo"),

    path('tags/',  TagsView.as_view(), name="tasks"),
    path('tags/<int:tags_id>/', TagsDetailsView.as_view(), name="todo_details"),
    
    path('create_user/', CreateUserView.as_view(), name="create_user"),
    path('create_token/', CreateTokenView.as_view(), name="login"),
    
    path('me/', ManageUserView.as_view(), name="me"),
    path('change_password/', ChangePasswordView.as_view(), name="change_password"),
    path('password_rest/', include("django_rest_passwordreset.urls"), name="password_reset"),

]