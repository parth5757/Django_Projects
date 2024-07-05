from django.shortcuts import redirect, render, HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, View, TemplateView,FormView
from app_modules.vendors.models import Vendor
from app_modules.product.models import Category, SubCategory, Brand, Product, WarehouseProductStock, WarehouseProductStockHistory, Barcode
from app_modules.company.models import Company
from django.db.models import Q
from django.views.generic import View
from django_datatables_too.mixins import DataTableMixin
from app_modules.company.models import Company, Warehouse
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse
from django.template.loader import get_template
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from app_modules.product.forms import (
    BrandCreateForm,CategoryCreateForm, CreateProductCSVForm, ImportProductCSVForm, 
    ProductPriceUpdateForm,ProductCreateForm,
    SubCategoryCreateForm, UpdateStockCSVForm, WarehouseStockForms, BarcodeForm)
from app_modules.vendors.models import Vendor
from barcode import EAN13, Code39
from django.core.files import File
from barcode.writer import ImageWriter
import uuid
from io import BytesIO


# Create your views here.
"""
Brand Model Crud(Created Date:-19/06/23)
"""


class BrandCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Brand
    form_class = BrandCreateForm
    success_message = "Brand Created Successfully!!"
    template_name = "product/form_brand.html"
    success_url = reverse_lazy("product:list_brand")


class BrandUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Brand
    form_class = BrandCreateForm
    success_message = "Brand Updated Successfully!!"
    template_name = "product/form_brand.html"
    success_url = reverse_lazy("product:list_brand")


class BrandListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = Brand
    template_name = "product/list_brand.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company_list"] = Company.objects.all()
        return context


class BrandDataTablesAjaxPagination(DataTableMixin, View):
    model = Brand

    def get_queryset(self):
        qs = Brand.objects.all()

        if self.request.user.role == "company admin":
            qs = Brand.objects.filter(
                company__id=self.request.user.get_company_id)

        company = self.request.GET.get("company")
        if company:
            qs = qs.filter(company__id=company)

        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs.order_by("id")

    def _get_actions(self, obj):
        """Get action buttons w/links."""
        update_url = reverse("product:update_brand", kwargs={"pk": obj.id})
        delete_url = reverse("product:delete_brand")
        return f'<center><a href="{update_url}" title="Edit"><i class="ft-edit font-medium-3 mr-2"></i></a> <label data-title="{obj.name}" title="Delete" data-url="{delete_url}" data-id="{obj.id}" id="delete_btn" class="danger p-0 ajax-delete-btn"><i class="ft-trash font-medium-3"></i></label></center>'

    def _get_product_count(self, obj):
        return Product.objects.filter(brand=obj).count()

    def filter_queryset(self, qs):
        if self.search:
            return qs.filter(
                Q(name__icontains=self.search) |
                Q(status__icontains=self.search)
            )
        return qs

    def _get_status(self, obj):
        t = get_template("product/get_brand_status.html")
        return t.render(
            {"product": obj, "request": self.request}
        )

    def prepare_results(self, qs):
        return [
            {
                'id': o.id,
                'name': o.name,
                'company': o.company.company_name,
                'status': self._get_status(o),
                'product_count': o.product_count,
                'active_product': o.active_product_count,
                'inactive_product': o.inactive_product_count,
                'actions': self._get_actions(o),
            }
            for o in qs
        ]

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)


class BrandDeleteAjaxView(View):
    def post(self, request):
        brand_id = self.request.POST.get("id")
        Brand.objects.filter(id=brand_id).delete()
        return JsonResponse({"message": "Brand Deleted Successfully."})


"""
Category Model Crud(Created Date:-19/06/23)
"""


class CategoryCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryCreateForm
    success_message = "Category Created Successfully!!"
    template_name = "product/form_category.html"
    success_url = reverse_lazy("product:list_category")


class CategoryUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryCreateForm
    success_message = "Category Updated Successfully!!"
    template_name = "product/form_category.html"
    success_url = reverse_lazy("product:list_category")


class CategoryListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = Category
    template_name = "product/list_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company_list"] = Company.objects.all()
        return context


class CategoryDataTablesAjaxPagination(DataTableMixin, View):
    model = Category
    # queryset=Category.objects.all()

    def get_queryset(self):
        qs = Category.objects.all()
        if self.request.user.role == "company admin":
            qs = Category.objects.filter(
                company__id=self.request.user.get_company_id)

        company = self.request.GET.get("company")
        if company:
            qs = qs.filter(company__id=company)

        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)

        return qs.order_by("id")

    def _get_actions(self, obj):
        """Get action buttons w/links."""
        update_url = reverse("product:update_category", kwargs={"pk": obj.id})
        delete_url = reverse("product:delete_category")
        return f'<center><a href="{update_url}" title="Edit"><i class="ft-edit font-medium-3 mr-2"></i></a> <label data-title="{obj.name}" title="Delete" data-url="{delete_url}" data-id="{obj.id}" id="delete_btn" class="danger p-0 ajax-delete-btn"><i class="ft-trash font-medium-3"></i></label></center>'

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        return qs.filter(Q(name__icontains=self.search)) if self.search else qs

    def _get_status(self, obj):
        t = get_template("product/get_category_status.html")
        return t.render(
            {"product": obj, "request": self.request}
        )

    def _get_type_invoice(self, obj):
        t = get_template("product/get_type_a_invoice.html")
        return t.render(
            {"product": obj, "request": self.request}
        )

    def prepare_results(self, qs):
        return [
            {
                'id': o.id,
                'name': o.name,
                'company': o.company.company_name,
                'status': self._get_status(o),
                'is_type_a_invoice': self._get_type_invoice(o),
                'product_count': o.product_count,
                'active_product': o.active_product_count,
                'inactive_product': o.inactive_product_count,
                'actions': self._get_actions(o),
            }
            for o in qs
        ]

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)


class CategoryDeleteAjaxView(View):
    def post(self, request):
        category_id = self.request.POST.get("id")
        Category.objects.filter(id=category_id).delete()

        return JsonResponse({"message": "Category Deleted Successfully ."})


"""
SubCategory Model Crud(Created Date:-19/06/23)
"""


class SubCategoryCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = SubCategory
    form_class = SubCategoryCreateForm
    success_message = "Subcategory Created Successfully!!"
    template_name = "product/form_subcategory.html"
    success_url = reverse_lazy("product:list_subcategory")

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["user"] = self.request.user
        return form_kwargs


class SubCategoryUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = SubCategory
    form_class = SubCategoryCreateForm
    success_message = "Subcategory Updated Successfully!!"
    template_name = "product/form_subcategory.html"
    success_url = reverse_lazy("product:list_subcategory")

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["user"] = self.request.user
        return form_kwargs


class SubCategoryListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = SubCategory
    template_name = "product/list_subcategory.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company_list"] = Company.objects.all()
        context["category_list"] = Category.objects.all()
        return context


class SubCategoryDataTablesAjaxPagination(DataTableMixin, View):
    model = SubCategory

    def get_queryset(self):
        qs = SubCategory.objects.all()
        if self.request.user.role == "company admin":
            qs = SubCategory.objects.filter(
                company__id=self.request.user.get_company_id)
        category = self.request.GET.get("category")
        if category:
            qs = qs.filter(category__id=category)

        company = self.request.GET.get("company")
        if company:
            qs = qs.filter(company__id=company)

        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)

        return qs.order_by("id")

    def _get_actions(self, obj):
        """Get action buttons w/links."""
        update_url = reverse("product:update_subcategory",
                             kwargs={"pk": obj.id})
        delete_url = reverse("product:delete_subcategory")

        return f'<center><a href="{update_url}" title="Edit"><i class="ft-edit font-medium-3 mr-2"></i></a> <label data-title="{obj.name}" title="Delete" data-url="{delete_url}" data-id="{obj.id}" id="delete_btn" class="danger p-0 ajax-delete-btn"><i class="ft-trash font-medium-3"></i></label></center>'

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(name__icontains=self.search) |
                Q(category__name__icontains=self.search)

            )
        return qs

    def _get_status(self, obj):
        t = get_template("product/get_subcategory_status.html")
        return t.render(
            {"product": obj, "request": self.request}
        )

    def _get_type_invoice(self, obj):
        t = get_template("product/get_type_a_invoice.html")
        return t.render(
            {"product": obj, "request": self.request}
        )

    def prepare_results(self, qs):
        return [
            {
                'id': o.id,
                'name': o.name,
                'category': o.category.name,
                'company': o.company.company_name,
                'status': self._get_status(o),
                'is_type_a_invoice': self._get_type_invoice(o),
                'product_count': o.product_count,
                'active_product': o.active_product_count,
                'inactive_product': o.inactive_product_count,
                'actions': self._get_actions(o),
            }
            for o in qs
        ]

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)


class SubCategoryDeleteAjaxView(View):
    def post(self, request):
        subcategory_id = self.request.POST.get("id")
        SubCategory.objects.filter(id=subcategory_id).delete()
        return JsonResponse({"message": "Subcategory Deleted Successfully."})


"""
Product Model Crud(Created Date:-19/06/23)
"""


class ProductCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductCreateForm
    success_message = "Product Created Successfully!!"
    template_name = "product/form_product.html"
    success_url = reverse_lazy("product:list_product")

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["user"] = self.request.user
        return form_kwargs


class LoadCategory(View):
    def get(self, request):
        data = {
            'category_list' : list(Category.objects.filter(company__id=request.GET.get('company_id')).values('id', 'name')),
            'vendor_list' : list(Vendor.objects.filter(company__id=request.GET.get('company_id')).values('id', 'first_name')),
            'brand_list' : list(Brand.objects.filter(company__id=request.GET.get('company_id')).values('id', 'name'))
        }
        return JsonResponse(data, safe=False)
    
class LoadSubCategory(View):
    def get(self, request):
        user=self.request.user.get_company_id
        if user:
            subcategory_list = list(SubCategory.objects.filter(
                category__id=request.GET.get('category_id'),company__id=user).values('id', 'name'))
        subcategory_list = list(SubCategory.objects.filter(
                category__id=request.GET.get('category_id'),company__id=request.GET.get('company_id')).values('id', 'name'))
        return JsonResponse(subcategory_list, safe=False)
    

class ProductUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductCreateForm
    success_message = "Product Updated Successfully!!"
    template_name = "product/form_product.html"
    success_url = reverse_lazy("product:list_product")

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["user"] = self.request.user
        return form_kwargs

class ProductListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = Product
    template_name = "product/list_product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_list"] = Category.objects.all()
        context["subcategory_list"] = SubCategory.objects.all()
        context["brand_list"] = Brand.objects.all()
        context["product_list"] = Product.objects.all()
        context["company_list"] = Company.objects.all()
        return context


class ProductDataTablesAjaxPagination(DataTableMixin, View):
    model = Product

    def get_queryset(self):
        qs = Product.objects.all()
        if self.request.user.role == "company admin":
            qs = Product.objects.filter(
                company__id=self.request.user.get_company_id)

        brand = self.request.GET.get("brand")
        if brand:
            qs = qs.filter(brand__id=brand)

        category = self.request.GET.get("category")
        if category:
            qs = qs.filter(category__id=category)

        subcategory = self.request.GET.get("subcategory")
        if subcategory:
            qs = qs.filter(subcategory__id=subcategory)

        company = self.request.GET.get("company")
        if company:
            qs = qs.filter(company__id=company)

        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)

        return qs.order_by("id")

    def _get_actions(self, obj):
        """Get action buttons w/links."""
        update_url = reverse("product:update_product", kwargs={"pk": obj.id})
        delete_url = reverse("product:delete_product")
        barcode_url = reverse("product:barcode", kwargs={"pk": obj.id})
        return f'<div class="row"><center>  <a href="{barcode_url}" title="Edit"><i class="ft-eye font-medium-3 mr-2"></i></a>  <a href="{update_url}" title="Edit"><i class="ft-edit font-medium-3 mr-2"></i></a>  <label data-title="{obj.name}" title="Delete" data-url="{delete_url}" data-id="{obj.id}" id="delete_btn" class="danger p-0 ajax-delete-btn"><i class="ft-trash font-medium-3"></i></label></center></div>'

    def _get_product_image(self, obj):
        t = get_template("product/get_product_image.html")
        return t.render(
            {
                "height": 30,
                "img_url": obj.product_image,
                "obj": obj,

            }
        )

    def _get_status(self, obj):
        t = get_template("product/get_product_status.html")
        return t.render(
            {"product": obj, "request": self.request}
        )

    def _get_type_invoice(self, obj):
        t = get_template("product/get_type_a_invoice.html")
        return t.render(
            {"product": obj, "request": self.request}
        )

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(name__icontains=self.search) |
                Q(category__name__icontains=self.search) |
                Q(subcategory__name__icontains=self.search) |
                Q(brand__name__icontains=self.search)
            )
        return qs

    def prepare_results(self, products):
        return [
            {
                # 'no' : index,
                'id': product.id,
                'name': product.name,
                'product_image': self._get_product_image(product),
                'company': product.company.company_name,
                'category': product.category.name,
                'subcategory': product.subcategory.name,
                'brand': product.brand.name,
                're_order_mark': product.re_order_mark,
                'is_apply_ml_quantity': product.is_apply_ml_quantity,
                'ml_quantity': product.ml_quantity,
                'is_apply_weight': product.is_apply_weight,
                'weight': product.weight,
                # 'stock': product.stock,
                'srp': product.srp,
                'status': self._get_status(product),
                'is_type_a_invoice': self._get_type_invoice(product),
                # 'description': f'{product.description[:10]}...',
                'actions': self._get_actions(product),
            }
            for product in products
        ]

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)


class ProductDeleteAjaxView(View):
    def post(self, request):
        product_id = self.request.POST.get("id")
        Product.objects.filter(id=product_id).delete()
        return JsonResponse({"message": "Product Deleted Successfully."})
    
class BarcodeView(LoginRequiredMixin, FormView):

    template_name = "product/add_barcode.html"
    form_class=BarcodeForm
    success_url = reverse_lazy("product:list_product")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('pk')
        product = Product.objects.filter(id=product_id).first()
        context["product"] = product
        return context
    
class BarcodeGenerateView(LoginRequiredMixin, View):

    def post(self,*args, **kwargs):
        product_name=self.request.POST.get('product_name')
        product = Product.objects.get(name=product_name)
        product_id=self.request.POST.get('product_id')
        product_type=self.request.POST.get('product_type')
        barcode_number=self.request.POST.get('barcode_number')

        buffer = BytesIO()
        my_code = Code39(barcode_number, writer=ImageWriter())
        my_code.write(buffer)

        if Barcode.objects.filter(barcode_number=barcode_number):                
            messages.add_message(self.request, messages.WARNING, "This Barcode Number's Barcode already Exixts")
            return HttpResponseRedirect(reverse('product:list_product'))
        
        Barcode.objects.create(product=product,product_type=product_type,barcode_number=barcode_number,barcode_code=File(buffer, name=f"{str(uuid.uuid4())}.png"))
        
        messages.add_message(self.request, messages.SUCCESS, "Barcode Created Successfully.")
        return HttpResponseRedirect(reverse('product:list_product'))
    
class ProdcutBarcodeDataTablesAjaxPagination(LoginRequiredMixin, DataTableMixin, View):
    model = Barcode

    def get_queryset(self):
        qs = Barcode.objects.all()
        product_id = self.request.GET.get("id")
        if product_id:
            qs = qs.filter(product__id=product_id)

        return qs

    # def _get_actions(self, obj):
    #     """Get action buttons w/links."""
        # update_url = reverse("product:update_product", kwargs={"pk": obj.id})
        # delete_url = reverse("product:delete_product")
        # return f'<div class="row"><center>  <a href="{barcode_url}" title="Edit"><i class="ft-eye font-medium-3 mr-2"></i></a>  <a href="{update_url}" title="Edit"><i class="ft-edit font-medium-3 mr-2"></i></a>  <label data-title="{obj.name}" title="Delete" data-url="{delete_url}" data-id="{obj.id}" id="delete_btn" class="danger p-0 ajax-delete-btn"><i class="ft-trash font-medium-3"></i></label></center></div>'

    def _get_barcode_image(self, obj):
        t = get_template("product/get_barcode_image.html")
        return t.render(
            {
                "height": 80,
                "width": 300,
                "img_url": obj.barcode_code,
                "obj": obj,

            }
        )



    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(barcode_number__icontains=self.search)
            )
        return qs

    def prepare_results(self, qs):
        return [
            {
                # 'no' : index,
                'id': o.id,
                'unit':o.product_type,
                'barcode_number': o.barcode_number,
                'barcode_code': self._get_barcode_image(o),
            }
            for o in qs
        ]

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)


class ProductPriceListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = Product
    template_name = "product/list_product_price.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_list"] = Category.objects.all()
        context["subcategory_list"] = SubCategory.objects.all()
        context["brand_list"] = Brand.objects.all()
        context["product_list"] = Product.objects.all()
        context["company_list"] = Company.objects.all()
        return context


class ProductPriceDataTablesAjaxPagination(DataTableMixin, View):
    model = Product
    # queryset=Product.objects.all()

    def get_queryset(self):
        qs = Product.objects.all()
        if self.request.user.role == "company admin":
            qs = Product.objects.filter(
                company__id=self.request.user.get_company_id)

        brand = self.request.GET.get("brand")
        if brand:
            qs = qs.filter(brand__id=brand)

        category = self.request.GET.get("category")
        if category:
            qs = qs.filter(category__id=category)

        subcategory = self.request.GET.get("subcategory")
        if subcategory:
            qs = qs.filter(subcategory__id=subcategory)

        company = self.request.GET.get("company")
        if company:
            qs = qs.filter(company__id=company)

        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)

        return qs.order_by("id")

    def _get_actions(self, obj):
        """Get action buttons w/links."""
        return f'<center><a href="{obj.id}/update/" title="Edit"><i class="ft-edit font-medium-3 mr-2"></i></a></center>'

    def _get_status(self, obj):
        t = get_template("product/get_product_status.html")
        return t.render(
            {"product": obj, "request": self.request}
        )

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        return qs.filter(Q(name__icontains=self.search)) if self.search else qs

    def prepare_results(self, qs):
        return [
            {
                'id': o.id,
                'name': o.name,
                'company': o.company.company_name,
                'cost_price': o.cost_price,
                'wholesale_min_price': o.wholesale_min_price,
                'wholesale_base_price': o.wholesale_base_price,
                'retail_min_price': o.retail_min_price,
                'retail_base_price': o.retail_base_price,
                'srp': o.srp,
                'status': self._get_status(o),
                'is_type_a_invoice': o.is_type_a_invoice,
                're_order_mark': o.re_order_mark,
                # 'description': f'{o.description[:10]}...',
                'actions': self._get_actions(o),
            }
            for o in qs
        ]

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)


class ProductPriceUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductPriceUpdateForm
    success_message = "Product Price Updated Successfully!!"
    template_name = "product/update_product_price.html"
    success_url = reverse_lazy("product:list_product_price")


class ManageProductStock(TemplateView):
    template_name = 'product/manage_product_stock.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company_list"] = Company.objects.all()
        user = self.request.user.company
        context["product_list_for_cadmin"] = Product.objects.filter(company__company_name=user,status=Product.ACTIVE)
        context["warehouse_list_for_cadmin"] = Warehouse.objects.filter(company__company_name=user,status=Warehouse.IS_ACTIVE)
        return context


class LoadWarehouse(View):
    def get(self, request):
        data = {
            'products_list': list(
                Product.objects.filter(
                    company__id=request.GET.get('id_company'),
                    status=Product.ACTIVE,
                ).values('id', 'name')
            ),
            'warehouse_list': list(
                Warehouse.objects.filter(
                    company__id=request.GET.get('id_company'),
                    status=Warehouse.IS_ACTIVE
                ).values('id', 'name')),
        }
        return JsonResponse(data, safe=False)


class WarehouseProuctstockUpdateView(FormView):
    form_class=WarehouseStockForms
    template_name = "product/warehouse_product_stock_update.html"
    success_url = reverse_lazy("product:list_product_price")
    success_message = "Product Price Updated Successfully!!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id=self.request.GET.get('product')
        product= Product.objects.get(id=product_id)
        warehouse_id=self.request.GET.get('warehouse')
        context["product"] = product
        context["warehouse_id"] = warehouse_id
        wharehousestock = WarehouseProductStock.objects.filter(warehouse__id=warehouse_id, product__id=product_id).first()
        context["available_stock"]=wharehousestock.stock if wharehousestock else 0
        return context
    
class UpdateStock(View):
    def post(self,*args, **kwargs):
        product_id=self.request.POST.get('product')
        product = Product.objects.get(id=product_id)
        warehouse_id=self.request.POST.get('warehouse')
        warehouse = Warehouse.objects.get(id=warehouse_id)
        piece=self.request.POST.get('stock')
        stock_obj, created= WarehouseProductStock.objects.get_or_create(product=product,warehouse=warehouse)
        if created:
            stock_obj.stock=int(piece)
        else:
            stock_obj.stock += int(piece)
        stock_obj.save()
        stock_history_obj=WarehouseProductStockHistory.objects.filter(product=product,warehouse=warehouse).last()
        stock_new_history_obj=WarehouseProductStockHistory.objects.create(product=product,warehouse=warehouse)
        if not stock_history_obj:
            stock_new_history_obj.before_stock=0
            stock_new_history_obj.stock=piece
        else:
            stock_new_history_obj.before_stock=stock_history_obj.stock
            stock_new_history_obj.stock=int(stock_history_obj.stock) + int(piece)
        stock_new_history_obj.affected_stock=piece
        stock_new_history_obj.save()
        messages.add_message(self.request, messages.SUCCESS, "Stock Updated Successfully.")
        return HttpResponseRedirect(reverse('product:manage_stocks'))
    

class ProductCreateFromCSVFormView(LoginRequiredMixin, FormView):
    template_name = "product/import_product.html"
    form_class = ImportProductCSVForm

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["user"] = self.request.user
        return form_kwargs

    def form_valid(self, form):
        # sourcery skip: extract-method, merge-dict-assign, remove-redundant-pass
        try:
            csv_file = self.request.FILES["csv_file"]
            file_data = csv_file.read().decode("utf-8")
            lines = file_data.split("\n")
            for line in lines[1:]:
                fields = line.split(",")
                if len(fields) > 25:
                    data_dict = {}
                    data_dict["name"] = fields[8]
                    company = Company.objects.get(company_name=fields[0])
                    data_dict["company"] = company
                    category, _ = Category.objects.get_or_create(name=fields[3], company=company)
                    category.description = fields[4]
                    category.is_type_a_invoice = str(fields[5]).lower() == "yes"
                    category.save()
                    data_dict["category"] = category
                    sub_category, _ = SubCategory.objects.get_or_create(name=fields[6], company=company, category=category)
                    sub_category.description = fields[7]
                    sub_category.save()
                    data_dict["subcategory"] = sub_category
                    brand, _ = Brand.objects.get_or_create(name=fields[1], company=company)
                    brand.description = fields[2]
                    brand.save()
                    data_dict["brand"] = brand
                    vendor, _ = Vendor.objects.get_or_create(email=fields[9], company=company)
                    data_dict["prefered_vendor"] = vendor
                    data_dict["is_apply_ml_quantity"] = str(fields[10]).lower() == "yes"
                    data_dict["ml_quantity"] = fields[11] if data_dict["is_apply_ml_quantity"] else 0
                    data_dict["is_apply_weight"] = str(fields[12]).lower() == "yes"
                    data_dict["weight"] = fields[13] if data_dict["is_apply_weight"] else 0
                    data_dict["box"] = str(fields[16]).lower() == "yes"
                    data_dict["box_piece"] = fields[17] if data_dict["box"] else 0
                    data_dict["case"] = str(fields[19]).lower() == "yes"
                    data_dict["case_piece"] = fields[20] if data_dict["case"] else 0
                    data_dict["case_upc"] = fields[18]
                    data_dict["srp"] = fields[21]
                    data_dict["status"] = "active"
                    data_dict["re_order_mark"] = fields[22]
                    data_dict["product_upc"] = fields[14]
                    data_dict["box_upc"] = fields[15]
                    data_dict["cost_price"] = fields[23]
                    # data_dict["box_cost_price"] = fields[25]
                    # data_dict["case_cost_price"] = fields[24]
                    data_dict["wholesale_min_price"] = fields[25]
                    # data_dict["case_wholesale_min_price"] = fields[27]
                    # data_dict["box_wholesale_min_price"] = fields[28]
                    data_dict["wholesale_base_price"] = fields[26]
                    # data_dict["case_wholesale_base_price"] = fields[30]
                    # data_dict["box_wholesale_base_price"] = fields[31]
                    data_dict["retail_min_price"] = fields[27]
                    # data_dict["case_retail_min_price"] = fields[33]
                    # data_dict["box_retail_min_price"] = fields[34]
                    data_dict["retail_base_price"] = fields[28]
                    # data_dict["case_retail_base_price"] = fields[36]
                    # data_dict["box_retail_base_price"] = fields[37]
                    data_dict["base_price"] = fields[24]
                    # data_dict["case_base_price"] = fields[39]
                    # data_dict["box_base_price"] = fields[40]
                    product_form = CreateProductCSVForm(data_dict)
                    if product_form.is_valid():
                        instance = product_form.save(commit=False)
                        instance.save()
                    else:
                        pass

            messages.add_message(self.request, messages.SUCCESS, "Product Uploaded Successfully.")
            return HttpResponseRedirect(reverse("product:list_product"))
        except Exception as e:
            import traceback
            print("exception::>>...", traceback.format_exc())
            messages.add_message(self.request, messages.WARNING, "Something went wrong, Please try again.")
            return HttpResponseRedirect(reverse("product:list_product"))


class AddStockFromCSVFormView(LoginRequiredMixin, FormView):
    template_name = "product/add_stock.html"
    form_class = ImportProductCSVForm

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["user"] = self.request.user
        return form_kwargs

    def form_valid(self, form):
        # sourcery skip: extract-method, merge-dict-assign, move-assign-in-block, remove-redundant-pass
        try:
            csv_file = self.request.FILES["csv_file"]
            file_data = csv_file.read().decode("utf-8")
            lines = file_data.split("\n")
            for line in lines[1:]:
                fields = line.split(",")
                data_dict = {}
                company = Company.objects.get(company_name=fields[0])
                warehouse, _ = Warehouse.objects.get_or_create(name=fields[1], company=company)
                data_dict["warehouse"] = warehouse
                category = Category.objects.get(name=fields[3], company=company)
                product, _ = Product.objects.get_or_create(name=fields[2], company=company, category=category)
                data_dict["product"] = product
                data_dict["stock"] = fields[4]
                stock_form = UpdateStockCSVForm(data_dict)
                if stock_form.is_valid():
                    instance = stock_form.save(commit=False)
                    instance.save()
                else:
                    pass

            messages.add_message(self.request, messages.SUCCESS, "Product Stock Updated Successfully.")
            return HttpResponseRedirect(reverse("product:manage_stocks"))
        except Exception as e:
            import traceback
            print("exception::>>...", traceback.format_exc())
            messages.add_message(self.request, messages.WARNING, "Something went wrong, Please try again.")
            return HttpResponseRedirect(reverse("product:manage_stocks"))
    
class ProdcutStockHistoryListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    model = WarehouseProductStockHistory
    template_name = "product/product_stock_history.html"


class ProdcutStockHistoryDataTablesAjaxPagination(DataTableMixin, View):
    model = WarehouseProductStockHistory

    def get_queryset(self):
        qs = WarehouseProductStockHistory.objects.all()

        # if self.request.user.role == "company admin":
        #     qs = WarehouseProductStockHistory.objects.filter(
        #         company__id=self.request.user.get_company_id)

        company = self.request.GET.get("company")
        if company:
            qs = qs.filter(warehouse__company__id=company)
        product = self.request.GET.get("product")
        if product:
            qs = qs.filter(product__id=product)

        warehouse = self.request.GET.get("warehouse")
        if warehouse:
            qs = qs.filter(warehouse__id=warehouse)
        return qs.order_by("id")
    
    def filter_queryset(self, qs):
        if self.search:
            return qs.filter(
                Q(product__name__icontains=self.search) |
                Q(warehouse__name__icontains=self.search)
            )
        return qs
    
    def prepare_results(self, qs):
        return [
            {
                'id': o.id,
                'created_at': o.created_at.date(),
                'warehouse': o.warehouse.name,
                'product': o.product.name,
                'before_stock': o.before_stock,
                'affected_stock': o.affected_stock,
                'stock': o.stock,
            }
            
            for o in qs
        ]

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)




    
    
    

    
