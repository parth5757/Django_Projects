from django.urls import path, include
from .views import MyLoginView, RegisterUser, ErrorView
from django.contrib.auth.views import (
    LogoutView
)

urlpatterns = [
    # Login Urls
    path('login/', MyLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
]
