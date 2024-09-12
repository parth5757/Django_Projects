"""
URL configuration for drf project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from drf_spectacular.views import SpectacularAPIView , SpectacularSwaggerView

urlpatterns = [
    # Admin
    path('api/admin/', admin.site.urls),
    
    # app
    path('api/app/', include('app.urls')),

    # Documentation for our api.
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),

    # JWT authentication.
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

]
