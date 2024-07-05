from django.urls import path
from app_modules.purchase_order.views import PurchaseOrderCreateView,GetVendorsAndProductsByCompanyAjax,AjaxGetProductDetails,AddProductInPurchaseList, PurchaseOrderListView,PurchaseOrderListAjax, PurchaseOrderUpdateView, AjaxGetUpdateProductDetails

app_name = "purchase_order"

urlpatterns = [
    path("create/",PurchaseOrderCreateView.as_view(),name="purchase_order_create"),
    path("ajax-get-vendors-by-company/",GetVendorsAndProductsByCompanyAjax.as_view(),name="ajax_get_vendors_by_company"),
    path("ajax-get-product-details/",AjaxGetProductDetails.as_view(),name="ajax_get_product_details"),
    path("ajax-add-product-in-purchase-list/",AddProductInPurchaseList.as_view(),name="add_product_in_purchase_list"),
    path("",PurchaseOrderListView.as_view(), name="purchase_order_list"),
    path("purchase_order/data-table-ajax",PurchaseOrderListAjax.as_view(), name="purchase_order_list_ajax"),
    path("<int:pk>/update",PurchaseOrderUpdateView.as_view(),name="purchase_order_update"),
    path("ajax-get-update-product-details/",AjaxGetUpdateProductDetails.as_view(),name="ajax_get_update_product_details"),
]