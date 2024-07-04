import factory

from drfecommerce.product.models import Category, Brand, Product

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = "test_category"
    