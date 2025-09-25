from rest_framework import serializers
from django.db import transaction

from .models import CartItem
from products.models import Product
from products.serializers import ProductListSerializer

class CartItemSerializer(serializers.ModelSerializer):
    """
    Full cart item serializer for displaying cart contents
    """
    product = ProductListSerializer(read_only=True)
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity', 'total_price', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'total_price')

class CartItemCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for adding items to cart
    """
    product_id = serializers.IntegerField()
    
    class Meta:
        model = CartItem
        fields = ('product_id', 'quantity')
    
    def validate_product_id(self, value):
        """Validate product exists and is active"""
        try:
            product = Product.objects.get(id=value, is_active=True)
            return value
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found or inactive.")
    
    def validate_quantity(self, value):
        """Validate quantity is positive"""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        if value > 100:  # Set reasonable limit
            raise serializers.ValidationError("Maximum quantity per item is 100.")
        return value
    
    def validate(self, data):
        """Validate stock availability"""
        try:
            product = Product.objects.get(id=data['product_id'])
            quantity = data['quantity']
            
            if quantity > product.stock:
                raise serializers.ValidationError(
                    f"Only {product.stock} items available in stock."
                )
            
            # Check if user already has this item in cart
            user = self.context['request'].user
            existing_cart_item = CartItem.objects.filter(
                user=user, 
                product_id=data['product_id']
            ).first()
            
            if existing_cart_item:
                total_quantity = existing_cart_item.quantity + quantity
                if total_quantity > product.stock:
                    available = product.stock - existing_cart_item.quantity
                    raise serializers.ValidationError(
                        f"You already have {existing_cart_item.quantity} of this item in cart. "
                        f"Only {available} more can be added."
                    )
            
            return data
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found.")

class CartUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating cart item quantity
    """
    class Meta:
        model = CartItem
        fields = ('quantity',)
    
    def validate_quantity(self, value):
        """Validate quantity is positive"""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        if value > 100:
            raise serializers.ValidationError("Maximum quantity per item is 100.")
        return value
    
    def validate(self, data):
        """Validate stock availability for the new quantity"""
        cart_item = self.instance
        new_quantity = data['quantity']
        
        if new_quantity > cart_item.product.stock:
            raise serializers.ValidationError(
                f"Only {cart_item.product.stock} items available in stock."
            )
        
        return data

class CartSummarySerializer(serializers.Serializer):
    """
    Serializer for cart summary data
    """
    item_count = serializers.IntegerField(read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    currency = serializers.CharField(read_only=True, default='USD')

class BulkCartUpdateSerializer(serializers.Serializer):
    """
    Serializer for bulk cart operations
    """
    items = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(),
            required=True
        ),
        min_length=1,
        max_length=50  # Reasonable limit
    )
    
    def validate_items(self, value):
        """Validate bulk update items format"""
        validated_items = []
        
        for item in value:
            if 'id' not in item or 'quantity' not in item:
                raise serializers.ValidationError(
                    "Each item must have 'id' and 'quantity' fields."
                )
            
            try:
                item_id = int(item['id'])
                quantity = int(item['quantity'])
            except (ValueError, TypeError):
                raise serializers.ValidationError(
                    "Item 'id' and 'quantity' must be integers."
                )
            
            if quantity <= 0:
                raise serializers.ValidationError(
                    "Quantity must be greater than 0."
                )
            
            validated_items.append({
                'id': item_id,
                'quantity': quantity
            })
        
        return validated_items

class CartToOrderSerializer(serializers.Serializer):
    """
    Serializer for converting cart to order (used in checkout)
    """
    shipping_address = serializers.CharField(max_length=500)
    phone_number = serializers.CharField(max_length=20)
    notes = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    
    def validate_phone_number(self, value):
        """Basic phone number validation"""
        import re
        if not re.match(r'^[\+]?[1-9][\d]{0,15}$', value.replace(' ', '').replace('-', '')):
            raise serializers.ValidationError("Invalid phone number format.")
        return value
    
    def validate(self, data):
        """Validate user has items in cart"""
        user = self.context['request'].user
        if not CartItem.objects.filter(user=user).exists():
            raise serializers.ValidationError("Cart is empty.")
        
        return data