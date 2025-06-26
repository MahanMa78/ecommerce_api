from django.http import JsonResponse
import stripe
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from .models import Cart, CartItem, Product ,Category, Review , WishList
from .serializers import CartItemSerializer, CartSerializer, ProductListSerializer  , ProductDetailSerializer , CategoryDetailSerializer ,CategoryListSerializer, ReviewSerializer, WishListSerializer


stripe.api_key = settings.STRIPE_SECRET_KEY
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



@api_view(["PUT"])
def update_review(request , pk):
    review = Review.objects.get(id=pk)
    rating = request.data.get("rating")
    review_text = request.data.get("review")
    
    review.rating = rating
    review.review = review_text
    review.save()
    
    serializer = ReviewSerializer(review)
    return Response(serializer.data)
    
    
@api_view(["DELETE"])
def delete_review(request , pk):
    review = Review.objects.get(id=pk)
    review.delete()
    
    return Response("Review deleted successfully!" , status=204)


@api_view(["DELETE"])
def delete_cartitem(request , pk):
    cartitem = CartItem.objects.get(id=pk)
    cartitem.delete()
    
    return Response("CartItem deleted successfully!" , status=204)


@api_view(["POST"])
def add_to_wishlist(request):
    product_id = request.data.get("product_id")
    email = request.data.get("email")
    user = User.objects.get(email=email)
    
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)
    
    
    wishlist = WishList.objects.filter(user=user,product=product)
    if wishlist:
        wishlist.delete()  
        return Response({"message": "WishList deleted successfully!"} , status=204)
    
    new_wishlist = WishList.objects.create(user=user, product=product)
    serializer = WishListSerializer(new_wishlist)
    return Response(serializer.data)


@api_view(['GET'])
def product_search(request):
    query = request.query_params.get("query")
    if not query:
        return Response("No Query Provided", status=400)
    
    products = Product.objects.filter(Q(name__icontains=query) | 
                                      Q(description__icontains=query) |
                                      Q(category__name__icontains=query))
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)
    if not products.exists():
        return Response({"error": "No products found"}, status=404)
    
    
    

@api_view(["POST"])
def create_checkout_session(request):
    cart_code = request.data.get("cart_code")
    email = request.data.get("email")
    cart = Cart.objects.get(cart_code=cart_code)
    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email= email,
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": item.product.name,
                        },
                        "unit_amount": int(item.product.price  * 100),
                    },
                    "quantity": item.quantity,
                }
                
                for item in cart.cartitems.all()
                
            ],
            mode="payment",
            # success_url="https://127.0.0.1:8000/success",
            # cancel_url="https://127.0.0.1:8000/cancel",
            
            success_url="https://next-shop-self.vercel.app/success",
            cancel_url="https://next-shop-self.vercel.app/failed",
        )
        return Response({"data": checkout_session})
    except Exception as e:
        return Response({"error": str(e)}, status=400)