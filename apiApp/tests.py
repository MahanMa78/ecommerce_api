from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import CustomUser , Product , Category

class ProductTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(
             email="testuser@email.com" 
        )
        
        cls.category = Category.objects.create(
            name = "Sport car"
        )
        
        
        cls.product = Product.objects.create(
            name = "Car 1" , 
            description = "good car" , 
            price = 120 ,
            category = cls.category
        )    

    def test_category_model_name(self):
        self.assertEqual(self.category.name , "Sport car")
    
    def test_product_model_name(self):
        self.assertEqual(self.product.name ,"Car 1" )
        
    def test_product_model_description(self):
        self.assertEqual(self.product.description , "good car")
        
    def test_product_model_price(self):
        self.assertEqual(self.product.price , 120)
     
    def test_product_model_description(self):
        self.assertEqual(self.product.category.name, "Sport car")
        
        
    