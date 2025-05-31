from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from .models import Cart, CartItem, Product ,Category, Review
from .serializers import CartItemSerializer, CartSerializer, ProductListSerializer  , ProductDetailSerializer , CategoryDetailSerializer ,CategoryListSerializer, ReviewSerializer


User = get_user_model()


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


@api_view(["POST"])
def add_to_cart(request):
    cart_code = request.data.get("cart_code")
    product_id = request.data.get("product_id")
    # quantity = request.data.get("quantity", 1) 
    
    # try:
    #     cart = Cart.objects.get(cart_code=cart_code)
    # except Cart.DoesNotExist:
    #     return Response({"error": "Cart not found"}, status=404)
    
    # try:
    #     product = Product.objects.get(id=product_id)
    # except Product.DoesNotExist:
    #     return Response({"error": "Product not found"}, status=404)
    
    # cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    # if created:
    #     cart_item.quantity = quantity
    #     cart_item.save()
    
    # * منتطق کد بالا برای اینکه اگه از متد get_or_creat نخوام استفاده کنم و بخوام زمانی که چیزی رو پیدا نمیکنه ازش استفاده کنم  هست البته ابن روش بالا تمیز تره ولی من با روش پایین توسعه رو ادامه میدم
    
    
    cart , created = Cart.objects.get_or_create(cart_code=cart_code)
    product = Product.objects.get(id=product_id)
    
    cartitem , created = CartItem.objects.get_or_create(cart=cart, product=product)
    cartitem.quantity = 1
    cartitem.save()
    
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(["PUT"])
def update_cartitem_quantity(request):
    cartitem_id = request.data.get('item_id')
    quantity = request.data.get("quantity")
    
    quantity = int(quantity)    
    
    cartitem = CartItem.objects.get(id=cartitem_id)
    cartitem.quantity = quantity
    cartitem.save()
    
    serializer = CartItemSerializer(cartitem)
    
    return Response({"data": serializer.data , "message" : "Cartitem updated successfully!"})
    
    
    
@api_view(["POST"])
def add_review(request):
    product_id = request.data.get("product_id")
    email = request.data.get("email")
    rating = request.data.get("rating")
    review_text = request.data.get("review")
    
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)
    
    user = User.objects.get(email=email)
    
    if Review.objects.filter(product=product , user=user).exists():
        return Response({"error": "You have already reviewed this product"}, status=400)
    
    review = Review.objects.create(product=product , user=user , rating=rating, review=review_text)
    serializer = ReviewSerializer(review)
    
    return Response(serializer.data)