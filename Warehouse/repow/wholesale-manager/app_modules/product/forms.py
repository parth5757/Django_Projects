from django import forms
from app_modules.vendors.models import Vendor
from app_modules.product.models import Category, SubCategory, Brand, Product, WarehouseProductStock, Barcode
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()



class BrandCreateForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(BrandCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label
        self.fields['description'].widget.attrs = {'class': 'form-control','rows': 4}
        self.fields["company"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields["status"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields['description'].required=False



                                                                             
class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CategoryCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label
        self.fields['description'].widget.attrs = {'class': 'form-control','rows': 4}
        self.fields['is_type_a_invoice'].widget.attrs = {'class': 'mt-1',}
        self.fields["company"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields["status"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields['description'].required=False





class SubCategoryCreateForm(forms.ModelForm):
    class Meta:
        model =   SubCategory
        fields = "__all__"

    def __init__(self,user, *args, **kwargs):
        super( SubCategoryCreateForm, self).__init__(*args, **kwargs)
        if user.role == User.COMPANY_ADMIN:
            self.fields["category"].queryset = Category.objects.filter(company__id=user.get_company_id)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label
        self.fields['description'].widget.attrs = {'class': 'form-control','rows': 4}
        self.fields['is_type_a_invoice'].widget.attrs = {'class': 'mt-1',}
        self.fields["company"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields["category"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields["status"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields['description'].required=False




                                                                             

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, user, *args, **kwargs):
        super( ProductCreateForm, self).__init__(*args, **kwargs)
        if user.role == User.COMPANY_ADMIN:
            self.fields["prefered_vendor"].queryset = Vendor.objects.filter(company__id=user.get_company_id)
            self.fields["category"].queryset = Category.objects.filter(company__id=user.get_company_id)

            self.fields["subcategory"].queryset = SubCategory.objects.filter(company__id=user.get_company_id)
            
            self.fields["brand"].queryset = Brand.objects.filter(company__id=user.get_company_id)
        
        if user.role == User.SUPER_ADMIN and self.instance.id:
            # self.fields["prefered_vendor"].queryset = Vendor.objects.filter(company__id=self.instance.company.id)
            self.fields["prefered_vendor"].queryset = Vendor.objects.all()
            self.fields["prefered_vendor"].initial = self.instance.prefered_vendor
            # self.fields["category"].queryset = Category.objects.filter(company__id=self.instance.company.id)
            self.fields["category"].queryset = Category.objects.all()
            self.fields["category"].initial = self.instance.category

            # self.fields["subcategory"].queryset = SubCategory.objects.filter(company__id=self.instance.company.id,category=self.instance.category)
            self.fields["subcategory"].queryset = SubCategory.objects.all()
            self.fields["subcategory"].initial = self.instance.subcategory

            # self.fields["brand"].queryset = Brand.objects.filter(company__id=self.instance.company.id)
            self.fields["brand"].queryset = Brand.objects.all()
            self.fields["brand"].initial = self.instance.brand

        # if user.role == User.SUPER_ADMIN and not self.instance.id:
        #     self.fields["prefered_vendor"].queryset = Vendor.objects.none()
        #     self.fields["category"].queryset = Category.objects.none()
        #     self.fields["subcategory"].queryset = SubCategory.objects.none()
        #     self.fields["brand"].queryset = Brand.objects.none()
        

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label
        self.fields['is_apply_ml_quantity'].widget.attrs = {'class': 'mt-2',}
        self.fields['is_apply_weight'].widget.attrs = {'class': 'mt-2',}
        self.fields['is_type_a_invoice'].widget.attrs = {'class': 'mt-2',}
        self.fields['box'].widget.attrs = {'class': 'mt-2',}
        self.fields['case'].widget.attrs = {'class': 'mt-2',}

        self.fields['ml_quantity'].required=False
        self.fields['weight'].required=False
        self.fields['box_piece'].required=False
        self.fields['case_piece'].required=False
        self.fields['re_order_mark'].required=False
        self.fields['product_image'].required=False

        self.fields["category"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields["subcategory"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields["brand"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields["company"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields["status"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields["prefered_vendor"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields["commission_code"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields["ml_quantity"].widget.attrs["placeholder"] = "0.0"
        self.fields["weight"].widget.attrs["placeholder"] = "0.0"
        self.fields["box_piece"].widget.attrs["placeholder"] = "0"
        self.fields["case_piece"].widget.attrs["placeholder"] = "0"
        # self.fields["product_image"].widget.attrs["class"] = "custom-file-input"
        self.fields["category"].widget.attrs["onchange"] = "loadSubcategory()"
        self.fields["company"].widget.attrs["onchange"] = "loadCategory()"

    def clean_ml_quantity(self):
        return self._extracted_from_clean_case_piece_2(
            'is_apply_ml_quantity', 'ml_quantity'
        )
    
    def clean_weight(self):
        return self._extracted_from_clean_case_piece_2('is_apply_weight', 'weight')
    
    def clean_box_piece(self):
        return self._extracted_from_clean_case_piece_2('box', 'box_piece')
    
    def clean_case_piece(self):
        return self._extracted_from_clean_case_piece_2('case', 'case_piece')
    
    def clean_product_upc(self):
        product_upc = self.cleaned_data.get("product_upc")
        box_upc = self.cleaned_data.get("box_upc")
        case_upc = self.cleaned_data.get("case_upc")

        if Product.objects.filter(Q(product_upc=product_upc) | Q(box_upc=product_upc) | Q(case_upc=product_upc)).exists():
            raise ValidationError("UPC already exists.")
        
        # if product_upc == box_upc or box_upc == case_upc or product_upc == case_upc:
        #     print("product_upc:::::", product_upc, box_upc, case_upc)
        #     raise ValidationError("Product UPC, Box UPC and Case UPC are not same.")

        return product_upc

    def clean_box_upc(self):
        product_upc = self.cleaned_data.get("product_upc")
        box_upc = self.cleaned_data.get("box_upc")
        case_upc = self.cleaned_data.get("case_upc")

        if Product.objects.filter(Q(product_upc=box_upc) | Q(box_upc=box_upc) | Q(case_upc=box_upc)).exists():
            raise ValidationError("UPC already exists.")
        
        # if product_upc == box_upc or box_upc == case_upc or product_upc == case_upc:
        #     print("box_upc:::::", product_upc, box_upc, case_upc)
        #     raise ValidationError("Product UPC, Box UPC and Case UPC are not same.")

        return box_upc

    def clean_case_upc(self):
        product_upc = self.cleaned_data.get("product_upc")
        box_upc = self.cleaned_data.get("box_upc")
        case_upc = self.cleaned_data.get("case_upc")

        if Product.objects.filter(Q(product_upc=case_upc) | Q(box_upc=case_upc) | Q(case_upc=case_upc)).exists():
            raise ValidationError("UPC already exists.")
        
        # if product_upc == box_upc or box_upc == case_upc or product_upc == case_upc:
        #     print("case_upc:::::", product_upc, box_upc, case_upc)
        #     raise ValidationError("Product UPC, Box UPC and Case UPC are not same.")

        return case_upc

    def clean(self):
        cleaned_data = self.cleaned_data
        product_upc = cleaned_data.get("product_upc")
        box_upc = cleaned_data.get("box_upc")
        case_upc = cleaned_data.get("case_upc")
        if product_upc == box_upc or box_upc == case_upc or product_upc == case_upc:
            print("------->>>>>>>>>>>>>")
            raise ValidationError({"case_upc": "Product UPC, Box UPC and Case UPC are not same."})
        return cleaned_data

    # `clean_ml_quantity`, `clean_weight`, `clean_box_piece` and `clean_case_piece`
    def _extracted_from_clean_case_piece_2(self, arg0, arg1):
        is_apply_ml_quantity = self.cleaned_data.get(arg0)
        ml_quantity = self.cleaned_data.get(arg1)
        return ml_quantity if is_apply_ml_quantity else 0.0
    
class ProductPriceUpdateForm(forms.ModelForm):
    class Meta:
        model =  Product
        # fields = ("name",)
        fields = ("name", "srp", "cost_price", "wholesale_min_price", "wholesale_base_price", "retail_min_price", "retail_base_price")

    def __init__(self, *args, **kwargs):
        super(ProductPriceUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = visible.field.label
        # self.fields['is_apply_ml_quantity'].widget.attrs = {'class': 'mt-1',}
        # self.fields['is_apply_weight'].widget.attrs = {'class': 'mt-1',}
        # self.fields['is_type_a_invoice'].widget.attrs = {'class': 'mt-1',}
        

class ImportProductCSVForm(forms.Form):
    csv_file = forms.FileField(widget=forms.FileInput(attrs={'accept': ".csv"}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ImportProductCSVForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

    def clean_csv_file(self):
        csv_file = self.cleaned_data["csv_file"]
        if not csv_file.name.endswith('.csv'):
            raise ValidationError("Only CSV file is accepted.")
        return csv_file


class CreateProductCSVForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ("company", "category", "subcategory", "name", "prefered_vendor", "brand", "is_apply_ml_quantity", "ml_quantity", "is_apply_weight", "weight", "srp", "status", "is_type_a_invoice", "cost_price", "wholesale_min_price", "wholesale_base_price", "retail_min_price", "retail_base_price", "box", "box_piece", "case", "case_piece", "re_order_mark", "product_upc", "box_upc", "case_upc", "base_price")                                                                          

    def clean_product_upc(self):
        product_upc = self.cleaned_data.get("product_upc")
        box_upc = self.cleaned_data.get("box_upc")
        case_upc = self.cleaned_data.get("case_upc")

        if Product.objects.filter(Q(product_upc=product_upc) | Q(box_upc=product_upc) | Q(case_upc=product_upc)).exists():
            raise ValidationError("UPC already exists.")
        
        # if product_upc == box_upc or box_upc == case_upc or product_upc == case_upc:
        #     print("product_upc:::::", product_upc, box_upc, case_upc)
        #     raise ValidationError("Product UPC, Box UPC and Case UPC are not same.")

        return product_upc

    def clean_box_upc(self):
        product_upc = self.cleaned_data.get("product_upc")
        box_upc = self.cleaned_data.get("box_upc")
        case_upc = self.cleaned_data.get("case_upc")

        if Product.objects.filter(Q(product_upc=box_upc) | Q(box_upc=box_upc) | Q(case_upc=box_upc)).exists():
            raise ValidationError("UPC already exists.")
        
        # if product_upc == box_upc or box_upc == case_upc or product_upc == case_upc:
        #     print("box_upc:::::", product_upc, box_upc, case_upc)
        #     raise ValidationError("Product UPC, Box UPC and Case UPC are not same.")

        return box_upc

    def clean_case_upc(self):
        product_upc = self.cleaned_data.get("product_upc")
        box_upc = self.cleaned_data.get("box_upc")
        case_upc = self.cleaned_data.get("case_upc")

        if Product.objects.filter(Q(product_upc=case_upc) | Q(box_upc=case_upc) | Q(case_upc=case_upc)).exists():
            raise ValidationError("UPC already exists.")
        
        # if product_upc == box_upc or box_upc == case_upc or product_upc == case_upc:
        #     print("case_upc:::::", product_upc, box_upc, case_upc)
        #     raise ValidationError("Product UPC, Box UPC and Case UPC are not same.")

        return case_upc

    def clean(self):
        cleaned_data = self.cleaned_data
        product_upc = cleaned_data.get("product_upc")
        box_upc = cleaned_data.get("box_upc")
        case_upc = cleaned_data.get("case_upc")
        if product_upc == box_upc or box_upc == case_upc or product_upc == case_upc:
            raise ValidationError("Product UPC, Box UPC and Case UPC are not same.")
        return cleaned_data


class AddStockCSVForm(forms.Form):
    csv_file = forms.FileField(widget=forms.FileInput(attrs={'accept': ".csv"}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AddStockCSVForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

    def clean_csv_file(self):
        csv_file = self.cleaned_data["csv_file"]
        if not csv_file.name.endswith('.csv'):
            raise ValidationError("Only CSV file is accepted.")
        return csv_file


class UpdateStockCSVForm(forms.ModelForm):

    class Meta:
        model = WarehouseProductStock
        fields = ("warehouse", "product", "stock")


class WarehouseStockForms(forms.Form):
    warehouse= forms.IntegerField()
    company= forms.IntegerField()
    stock= forms.IntegerField()

    
                                                                             
class BarcodeForm(forms.ModelForm):
    class Meta:
        model = Barcode
        fields = ("__all__")

    def __init__(self, *args, **kwargs):
        
        super(BarcodeForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label