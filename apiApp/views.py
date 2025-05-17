from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from .models import Product ,Category
from .serializers import ProductListSerializer  , ProductDetailSerializer , CategoryDetailSerializer ,CategoryListSerializer

@api_view(['GET'])
def product_list(request):
    products = Product.objects.filter(featured=True)   
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)
    
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data) 


@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategoryListSerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def category_detail(request, slug):
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=404)
    
    serializer = CategoryDetailSerializer(category)
    return Response(serializer.data)