from rest_framework import serializers
from products.serializers import ProductListSerializer
from orders.models import OrderItem, Order
from cart.models import CartItem




class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity', 'price', 'total_price')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    order_number = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = (
            'id', 'order_number', 'total_amount', 'status', 'shipping_address',
            'phone_number', 'items', 'created_at', 'updated_at'
        )

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('shipping_address', 'phone_number')

    def create(self, validated_data):
        user = self.context['request'].user
        
        # Get user's cart items
        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            raise serializers.ValidationError("Cart is empty.")
        
        # Calculate total amount
        total_amount = sum(item.total_price for item in cart_items)
        
        # Create order
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            **validated_data
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            
            # Update product stock
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()
        
        # Clear cart
        cart_items.delete()
        
        return order

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('status',)


