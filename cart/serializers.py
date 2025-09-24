from rest_framework import serializers
from .models import CartItem,Product
from serializers import ProductListSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_id', 'quantity', 'total_price', 'created_at')

    def validate_product_id(self, value):
        try:
            product = Product.objects.get(id=value, is_active=True)
            if not product.is_in_stock():
                raise serializers.ValidationError("Product is out of stock.")
            return value
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found.")

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value

class CartItemCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ('product_id', 'quantity')

    def validate_product_id(self, value):
        try:
            product = Product.objects.get(id=value, is_active=True)
            if not product.is_in_stock():
                raise serializers.ValidationError("Product is out of stock.")
            return value
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found.")

    def validate(self, data):
        user = self.context['request'].user
        product_id = data['product_id']
        quantity = data['quantity']
        
        try:
            product = Product.objects.get(id=product_id)
            if quantity > product.stock:
                raise serializers.ValidationError("Not enough stock available.")
        except Product.DoesNotExist:
            pass  # Already handled in validate_product_id
        
        return data


