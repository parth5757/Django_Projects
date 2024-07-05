from django.db import models
from app_modules.base.models import BaseModel
from app_modules.vendors.models import Vendor
from app_modules.company.models import Company,Warehouse
from app_modules.customers.validators import validate_file_extension

# Create your models here.


class Brand(BaseModel):
    ACTIVE = "active"
    INACTIVE = "inactive"

    STATUS_CHOICES = (
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive"),
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Brand Name'
    )

    company = models.ForeignKey(
        Company,
        verbose_name="Company",
        on_delete=models.CASCADE,
        related_name="brand_company"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        verbose_name='Status',
        default=ACTIVE
    )

    description = models.TextField(
        max_length=150,
        verbose_name="Description",
        null=True, blank=True
    )

    def __str__(self):
        return f'{self.name}{str(self.id)}'

    @property
    def product_count(self):
        return Product.objects.filter(brand__id=self.id).count()

    @property
    def active_product_count(self):
        return Product.objects.filter(
            brand__id=self.id, status=Product.ACTIVE).count()

    @property
    def inactive_product_count(self):
        return Product.objects.filter(
            brand__id=self.id, status=Product.INACTIVE).count()


class Category(BaseModel):
    ACTIVE = "active"
    INACTIVE = "inactive"

    STATUS_CHOICES = (
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive"),
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Category Name'
    )

    company = models.ForeignKey(
        Company,
        verbose_name="Company",
        on_delete=models.CASCADE,
        related_name="category_company"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        verbose_name='Status',
        default=ACTIVE)

    is_type_a_invoice = models.BooleanField(
        verbose_name="Is Type A Invoice", default=False
    )

    description = models.TextField(
        max_length=150,
        verbose_name="Description",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    @property
    def product_count(self):
        return Product.objects.filter(category__id=self.id).count()

    @property
    def active_product_count(self):
        return Product.objects.filter(
            category__id=self.id, status=Product.ACTIVE).count()

    @property
    def inactive_product_count(self):
        return Product.objects.filter(
            category__id=self.id, status=Product.INACTIVE).count()


class SubCategory(BaseModel):
    ACTIVE = "active"
    INACTIVE = "inactive"

    STATUS_CHOICES = (
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive"),
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Subcategory Name'
    )

    company = models.ForeignKey(
        Company,
        verbose_name="Company",
        on_delete=models.CASCADE,
        related_name="subcategory_company"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,

    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        verbose_name='Status',
        default=ACTIVE)

    is_type_a_invoice = models.BooleanField(
        verbose_name="Is Type A Invoice",
        default=False
    )

    description = models.TextField(
        max_length=150,
        verbose_name="Description",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    @property
    def product_count(self):
        return Product.objects.filter(subcategory__id=self.id).count()

    @property
    def active_product_count(self):
        return Product.objects.filter(
            subcategory__id=self.id, status=Product.ACTIVE).count()

    @property
    def inactive_product_count(self):
        return Product.objects.filter(
            subcategory__id=self.id, status=Product.INACTIVE).count()

class Product(BaseModel):

    ACTIVE = "active"
    INACTIVE = "inactive"

    STATUS_CHOICES = (
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive"),
    )

    COMMISSION_CODE_CHOICES = (
        (0.00, "0.00%"),
        (0.01, "0.01%"),
        (1.00, "1.00%"),
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="product_category"
    )

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name="product_subcategory"

    )

    name = models.CharField(
        max_length=50,
        verbose_name='Product Name'
    )

    prefered_vendor = models.ForeignKey(Vendor,
        verbose_name="Prefered Vendor",
        on_delete=models.CASCADE,
        related_name="product_vendor")

    product_image = models.ImageField(
        verbose_name="Product Image",
        upload_to='product-images',
        height_field=None,
        width_field=None,

    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="product_brand"

    )

    re_order_mark = models.PositiveIntegerField(
        verbose_name="Re Order Mark (Pieces)"
    )

    is_apply_ml_quantity = models.BooleanField(
        verbose_name="Is Apply ML Quantity",
        default=False
    )

    ml_quantity = models.FloatField(
        verbose_name="ML Quantity",
        
        default=0.00
    )

    is_apply_weight = models.BooleanField(
        verbose_name="Is Apply Weight (OZ)",
        default=False
    )

    weight = models.FloatField(
        verbose_name="Weight (Oz)",
        
        default=0.00
    )

    commission_code = models.FloatField(
        verbose_name="Commission Code",
        choices=COMMISSION_CODE_CHOICES,
        default=0.00
    )

    # stock = models.PositiveIntegerField(
    #     verbose_name="Stock(Pieces)",
    #     
    #     default=0)

    srp = models.FloatField(
        verbose_name="SRP(Suggested Retail Price)"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        verbose_name='Status',
        default=False)

    is_type_a_invoice = models.BooleanField(
        verbose_name="Is Type A Invoice",
        default=False
    )

    product_upc = models.PositiveBigIntegerField(
        verbose_name="Product UPC",
        default=0,
    )

    box_upc = models.PositiveBigIntegerField(
        verbose_name="Box UPC",
        default=0
    )

    case_upc = models.PositiveBigIntegerField(
        verbose_name="Case UPC",
        default=0
    )

    cost_price = models.FloatField(
        verbose_name="Cost Price",
        default=0.00
    )

    # box_cost_price = models.FloatField(
    #     verbose_name="Box Cost Price",
    #     default=0.00
    # )

    # case_cost_price = models.FloatField(
    #     verbose_name="Case Cost Price",
    #     default=0.00
    # )

    wholesale_min_price = models.FloatField(
        verbose_name="Wholesale Min Price",
        default=0.00
    )

    # box_wholesale_min_price = models.FloatField(
    #     verbose_name="Box Wholesale Min Price",
    #     default=0.00
    # )

    # case_wholesale_min_price = models.FloatField(
    #     verbose_name="Case Wholesale Min Price",
    #     default=0.00
    # )

    wholesale_base_price = models.FloatField(
        verbose_name="Wholesale Base Price",
        default=0.00
    )

    # box_wholesale_base_price = models.FloatField(
    #     verbose_name="Box Wholesale Base Price",
    #     default=0.00
    # )

    # case_wholesale_base_price = models.FloatField(
    #     verbose_name="Case Wholesale Base Price",
    #     default=0.00
    # )

    retail_min_price = models.FloatField(
        verbose_name="Retail Min Price",
        default=0.00
    )

    # box_retail_min_price = models.FloatField(
    #     verbose_name="Box Retail Min Price",
    #     default=0.00
    # )

    # case_retail_min_price = models.FloatField(
    #     verbose_name="Case Retail Min Price",
    #     default=0.00
    # )

    retail_base_price = models.FloatField(
        verbose_name="Retail Base Price",
        default=0.00
    )

    # box_retail_base_price = models.FloatField(
    #     verbose_name="Box Retail Base Price",
    #     default=0.00
    # )

    # case_retail_base_price = models.FloatField(
    #     verbose_name="Case Retail Base Price",
    #     default=0.00
    # )

    base_price = models.FloatField(
        verbose_name="Piece Base Price",
        default=0.00
    )

    # box_base_price = models.FloatField(
    #     verbose_name="Box Base Price",
    #     default=0.00
    # )

    # case_base_price = models.FloatField(
    #     verbose_name="Case Base Price",
    #     default=0.00
    # )

    box = models.BooleanField(
        verbose_name="Box",
        default=False
    )
    box_piece = models.IntegerField(
        verbose_name="Pieces in Box",
        default=0

    )

    case = models.BooleanField(
        verbose_name="Case",
        default=False
    )
    case_piece = models.IntegerField(
        verbose_name="Pieces in Case",
        default=0

    )

    company = models.ForeignKey(
        Company,
        verbose_name="Company",
        on_delete=models.CASCADE,
        related_name="product_company"
    )

    def __str__(self):
        return self.name


class WarehouseProductStock(BaseModel):

    warehouse=models.ForeignKey(
        Warehouse,
        verbose_name="Warehouse",
        related_name="warehouse_stock",
        on_delete=models.CASCADE)
    
    product=models.ForeignKey(
        Product,
        verbose_name="Product",
        related_name="product_stock",
        on_delete=models.CASCADE)
    
    stock = models.PositiveIntegerField(
        verbose_name="Stock(Pieces)",
        
        default=0)  
    
class WarehouseProductStockHistory(BaseModel):

    warehouse=models.ForeignKey(
        Warehouse,
        verbose_name="Warehouse",
        related_name="warehouse_stock_history",
        on_delete=models.CASCADE)
    
    product=models.ForeignKey(
        Product,
        verbose_name="Product",
        related_name="product_stock_history",
        on_delete=models.CASCADE)
    
    before_stock = models.PositiveIntegerField(
        verbose_name="Before Stock(Pieces)",
        default=0)
    
    affected_stock = models.IntegerField(
        verbose_name="Affected Stock(Pieces)",
        default=0)
    
    stock = models.PositiveIntegerField(
        verbose_name="Current Stock(Pieces)",
        default=0)

    remark = models.TextField(
        verbose_name="Remark",
        null= True,
        blank=True,
    ) 


class Barcode(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_barcode")
    product_type = models.CharField(verbose_name="Product Type", max_length=10 )
    barcode_number = models.CharField(unique=True, max_length=255)
    barcode_code = models.FileField(upload_to='product-barcode', validators=[validate_file_extension])