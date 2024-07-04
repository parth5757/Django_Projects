from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Category, Brand, Product
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer
    
class CategoryViewSet(viewsets.ViewSet):
    """
    A simple viewsets for view all categories
    """

    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class BrandViewSet(viewsets.ViewSet):
    """
    A simple viewsets for all Brand
    """

    queryset = Brand.objects.all()
    # print(queryset)
    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
class ProductViewSet(viewsets.ViewSet):
    """
    A simple viewsets for all Brand
    """

    queryset = Product.objects.all()
    # print(queryset)
    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)