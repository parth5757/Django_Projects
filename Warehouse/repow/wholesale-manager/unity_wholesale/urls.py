"""unity_wholesale URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from app_modules.users.views import HomeView
 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("company/", include('app_modules.company.urls'), name="company"),
    path("product/",include("app_modules.product.urls")),
    path("users/", include('app_modules.users.urls')),
    path("vendors/", include('app_modules.vendors.urls')),
    path("accounts/", include("allauth.urls")),
    path("", HomeView.as_view(), name="home_view"),
    path("customers/", include('app_modules.customers.urls'), name="customers"),
    path("purchase-order/",include('app_modules.purchase_order.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
