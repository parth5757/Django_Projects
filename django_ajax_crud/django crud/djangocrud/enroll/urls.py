from django.urls import path
from .views import RegisterTeacher
from . import views
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [

    path('', views.home, name='home'),
    # Authentication
    path('login/', LoginView.as_view(template_name='enroll/login.html'), name="user-login"),
    path('logout/', LogoutView.as_view(), name="user-logout"),
    path('register/', RegisterTeacher.as_view(), name='register'),
    # Crud student
    path('save/', views.save_data, name="save"),
    path('delete/', views.delete_data, name="delete"),
    path('edit/',views.edit_data, name="edit"),
    path('<str:undefined_route>/', views.error, name='error')
]