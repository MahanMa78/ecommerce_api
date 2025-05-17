from django.contrib import admin
from .models import Product , CustomUser , Category
from django.contrib.auth.admin import UserAdmin 


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff') #is_staff
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')
    ordering = ('username',)
admin.site.register(CustomUser, CustomUserAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'featured') #category
    search_fields = ('name', 'description')
    list_filter = ('featured', 'category')
    ordering = ('name',)
admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    ordering = ('name',)
admin.site.register(Category, CategoryAdmin)