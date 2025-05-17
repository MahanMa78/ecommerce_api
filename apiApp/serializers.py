from rest_framework import serializers
from .models import Category, Product 

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['id', 'name', 'slug' , 'image' ,'price']
        

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['id', 'name', 'slug' , 'image' ,'price', 'description']        

        
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = '__all__'
        fields = ['id', 'name', 'image' , 'slug']
        
        
class CategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        # fields = '__all__'
        fields = ['id', 'name', 'image', 'products']
        
        
