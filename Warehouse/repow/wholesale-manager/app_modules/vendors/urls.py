from django.urls import path
from app_modules.vendors.views import VendorCreateView, VendorDataTablesAjaxPagination, VendorDeleteAjaxView, VendorListView, VendorUpdateView

app_name = "vendors"

urlpatterns = [
    # url for user
    path("", VendorListView.as_view(), name="vendor_list"),
    path("create/", VendorCreateView.as_view(), name="vendor_create"),
    path("<int:pk>/update/", VendorUpdateView.as_view(), name="vendor_update"),
    path("vendor-delete-ajax/", VendorDeleteAjaxView.as_view(), name="vendor_delete"),
    path('vendor-list-ajax/', VendorDataTablesAjaxPagination.as_view(), name='vendor_list_ajax'),
]
    