from rest_framework import serializers
from .models import Cart, CartItem, Category, Product, Review ,WishList
from django.contrib.auth import get_user_model


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
        
        
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    sub_total = serializers.SerializerMethodField()
    class Meta:
        model = CartItem 
        fields = ["id" , 'product' , 'quantity' , 'sub_total']
        
        
    def get_sub_total(self , cartitem):
        total = cartitem.product.price * cartitem.quantity
        return total
    

class CartSerializer(serializers.ModelSerializer):
    cartitems = CartItemSerializer(read_only=True , many=True)
    # cart = serializers.PrimaryKeyRelatedField(read_only=True)
    cart_total = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ["id" , 'cart_code' , "cartitems", 'cart_total']
        
    def get_cart_total(self , cart):
        # total = 0
        # for item in cart.cartitems.all():
        #     total += item.product.price * item.quantity
        # return total
        items = cart.cartitems.all()
        total = sum(item.product.price * item.quantity for item in items)
        # total = sum([items.quantity * item.product.price for item in items])
        return total
        

class CartStatSerializer(serializers.ModelSerializer):
    cartitems = CartItemSerializer(read_only=True , many=True)
    total_quantity = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id' , 'cart_code' , 'total_quantity']
                
        def get_total_quantity(self , cart):
            items = cart.cartitems.all()
            total = sum(item.quantity for item in items)
            return total
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "first_name", "last_name","profile_picture_url"]        

        
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ["id","user","rating","review","created", "updated"]
        
        

class WishListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductListSerializer(read_only=True)
    class Meta:
        model = WishList
        fields = ['id', 'user', 'product', 'created']
        
    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     product = validated_data['product']
    #     wishlist_item, created = get_user_model().wishlist.through.objects.get_or_create(user=user, product=product)
    #     return wishlist_item