from django.urls import path
from app_modules.company.views import CompanyListView,CompanyCreateView,CompanyUpdateView,WarehouseListView,WarehouseCreateView,WarehouseUpdateView,CompanyListAjax,WarehouseListAjax,WarehouseDeleteAjaxView

app_name = "company"

urlpatterns = [
    # url for companies
    path("",CompanyListView.as_view(), name="company_list"),
    path("add/",CompanyCreateView.as_view(), name="add_company"),
    path("<int:pk>/update/",CompanyUpdateView.as_view(), name="update_company"),
    path("data-table-ajax/",CompanyListAjax.as_view(), name="company_list_ajax"),


    # url for warehouse
    path("warehouses/",WarehouseListView.as_view(), name="warehouse_list"),
    path("warehouses/add/",WarehouseCreateView.as_view(), name="add_warehouse"),
    path("warehouses/<int:pk>/update/",WarehouseUpdateView.as_view(), name="update_warehouse"),
    path("warehouses/data-table-ajax",WarehouseListAjax.as_view(),name="warehouse_list_ajax"),
    path("warehouses/data-delete-ajax",WarehouseDeleteAjaxView.as_view(),name="warehouse_delete_ajax"),

]