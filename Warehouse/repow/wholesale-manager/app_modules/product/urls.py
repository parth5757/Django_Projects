from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from app_modules.product.views import (
    AddStockFromCSVFormView,
    BrandListView,
    BrandCreateView,
    BrandUpdateView,
    BrandDataTablesAjaxPagination,
    BrandDeleteAjaxView,

    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDataTablesAjaxPagination,
    CategoryDeleteAjaxView,
    ProductCreateFromCSVFormView,

    SubCategoryListView,
    SubCategoryCreateView,
    SubCategoryUpdateView,
    SubCategoryDataTablesAjaxPagination,
    SubCategoryDeleteAjaxView,

    ProductListView,
    ProductCreateView,
    LoadSubCategory,
    LoadCategory,
    ProductUpdateView,
    ProductDataTablesAjaxPagination,
    ProductDeleteAjaxView,

    ProductPriceListView,
    ProductPriceDataTablesAjaxPagination,
    ProductPriceUpdateView,

    ManageProductStock,
    LoadWarehouse,
    WarehouseProuctstockUpdateView,
    UpdateStock,
    ProdcutStockHistoryListView,
    ProdcutStockHistoryDataTablesAjaxPagination,

    BarcodeView,
    BarcodeGenerateView,
    ProdcutBarcodeDataTablesAjaxPagination,
)


app_name = "product"

urlpatterns = [

     path("brands/", BrandListView.as_view(), name="list_brand"),
     path("brands/add/", BrandCreateView.as_view(), name="add_brand"),
     path("brands/<str:pk>/update/",
          BrandUpdateView.as_view(), name="update_brand"),
     path('brands/ajax/',
          BrandDataTablesAjaxPagination.as_view(), name='brands-list-ajax'),
     path("brand-delete-ajax/", BrandDeleteAjaxView.as_view(), name="delete_brand"),


     path("categories/", CategoryListView.as_view(), name="list_category"),
     path("categories/add/",
          CategoryCreateView.as_view(), name="add_category"),
     path("categories/<str:pk>/update/",
          CategoryUpdateView.as_view(), name="update_category"),
     path('categories/ajax/',
          CategoryDataTablesAjaxPagination.as_view(), name='category-list-ajax'),
     path("category-delete-ajax/", CategoryDeleteAjaxView.as_view(), name="delete_category"),


     path("subcategories/",
          SubCategoryListView.as_view(), name="list_subcategory"),
     path("subcategories/add/",
          SubCategoryCreateView.as_view(), name="add_subcategory"),
     path("subcategories/<str:pk>/update/",
          SubCategoryUpdateView.as_view(), name="update_subcategory"),
     path('subcategories/ajax/',
          SubCategoryDataTablesAjaxPagination.as_view(), name='subcategory-list-ajax'),
     path("subcategory-delete-ajax/", SubCategoryDeleteAjaxView.as_view(), name="delete_subcategory"),

     path("", ProductListView.as_view(), name="list_product"),
     path("add/", ProductCreateView.as_view(), name="add_product"),
     path("<str:pk>/update/",
          ProductUpdateView.as_view(), name="update_product"),
     path('add/load_subcategory/',LoadSubCategory.as_view(),
         name='load_subcategory'),

     path('load_category/',LoadCategory.as_view(),
         name='load_category'),
     
      
     path("ajax/",
          ProductDataTablesAjaxPagination.as_view(), name='product-list-ajax'),

     path("price/", ProductPriceListView.as_view(),
          name="list_product_price"),
     path('price/ajax/',
          ProductPriceDataTablesAjaxPagination.as_view(), name='product-price-list-ajax'),
     path("price/<str:pk>/update/",
          ProductPriceUpdateView.as_view(), name="update_product_price"),
     path("product-delete-ajax/", ProductDeleteAjaxView.as_view(), name="delete_product"),
         
     path("product-create-from-csv/", ProductCreateFromCSVFormView.as_view(), name="product_create_from_csv"),
     path("add-stock-from-csv/", AddStockFromCSVFormView.as_view(), name="add_stock_from_csv"),
     path("manage_stocks/", ManageProductStock.as_view(), name="manage_stocks"),
     path('manage_stocks/load_warehouse/',LoadWarehouse.as_view(),
         name='load_warehouse'),
     path('manage_stocks/get_form/',WarehouseProuctstockUpdateView.as_view(),
         name='get_form'),
     path('manage_stocks/update_stock/',UpdateStock.as_view(),
         name='update_stock'),

     path("list_product_history/",
          ProdcutStockHistoryListView.as_view(), name="list_product_history"),
     path("list_product_history/ajax/",
          ProdcutStockHistoryDataTablesAjaxPagination.as_view(), name='stock_history'),

     path('<int:pk>/barcode/', BarcodeView.as_view(), name="barcode"),
     path('generate-barcode/barcode/', BarcodeGenerateView.as_view(), name="generate_barcode"),
     path("product-barcode-list/ajax/",ProdcutBarcodeDataTablesAjaxPagination.as_view(), name="product_barcode_list")
     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
