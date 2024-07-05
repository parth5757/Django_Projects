from django.urls import path
from app_modules.customers import views

app_name = "customer"

urlpatterns = [
    # '''url for Customer model'''
    path("", views.CustomerListView.as_view(), name="customer_list"),
    path("create/", views.CustomerCreateView.as_view(), name="customer_create"),
    path('customer-list-ajax/', views.CustomerDataTablesAjaxPagination.as_view(), name='customer_list_ajax'),
    path("<int:pk>/update/", views.CustomerUpdateView.as_view(), name="customer_update"),
    path("delete/", views.CustomerDeleteAjaxView.as_view(), name="customer_delete"),


    # '''url for Payment model'''
    path("payment/", views.PaymentListView.as_view(), name="payment_list"),
    path("payment/create/", views.PaymentCreateView.as_view(), name="payment_create"),
    path('payment-list-ajax/', views.PaymentDataTablesAjaxPagination.as_view(), name='payment_list_ajax'),
    path("payment/<int:pk>/update/", views.PaymentUpdateView.as_view(), name="payment_update"),
    path("payment/delete/", views.PaymentDeleteAjaxView.as_view(), name="payment_delete"),

    # '''url for Sales Route model'''
    path("sales-route/", views.SalesRouteListView.as_view(), name="sales_route_list"),
    path("sales-route/create/", views.SalesRouteCreateView.as_view(), name="sales_route_create"),
    path('sales-route-list-ajax/', views.SalesRouteDataTablesAjaxPagination.as_view(), name='sales_route_list_ajax'),
    path("sales-route/<int:pk>/update/", views.SalesRouteUpdateView.as_view(), name="sales_route_update"),
    path("sales-route/delete/", views.SalesRouteDeleteAjaxView.as_view(), name="sales_route_delete"),

    # '''url for Price Level model'''
    path("price-level/", views.PricelevelListView.as_view(), name="price_level_list"),
    path("price-level/create/", views.PricelevelCreateView.as_view(), name="price_level_create"),
    path('price-level-list-ajax/', views.PricelevelDataTablesAjaxPagination.as_view(), name='price_level_list_ajax'),
    path("price-level/<int:pk>/update/", views.PricelevelUpdateView.as_view(), name="price_level_update"),
    path("price-level/delete/", views.PricelevelDeleteAjaxView.as_view(), name="price_level_delete"),

    #'''url for Product Price level'''
    path('price-level-product-ajax/', views.PricelevelProductDataTablesAjaxPagination.as_view(), name='price_level_product_list'),
    path('price-level-product-update-ajax/', views.PricelevelProductUpdateDataTablesAjaxPagination.as_view(), name='price_level_product_update'),
]