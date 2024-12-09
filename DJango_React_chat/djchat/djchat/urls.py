from django.contrib import admin
from django.urls import path
from drf_spectacular.views  import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from server.views import ServerListViewSet

router = DefaultRouter()
router.register("api/server/select", ServerListViewSet)
# router.register("api/docs/schema/ui/")

    
urlpatterns = [ 
    path("admin/", admin.site.urls),
    path("api/docs/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/schema/ui/", SpectacularSwaggerView.as_view(), name="")
] + router.urls