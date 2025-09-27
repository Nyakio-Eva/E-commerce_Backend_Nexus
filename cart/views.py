from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

# Import shared functionality from core
from core.permissions import IsOwnerOrReadOnly
# from core.utils import calculate_cart_total, send_cart_notification  
# from core.pagination import StandardResultsSetPagination

# Local app imports
from .models import CartItem
from .serializers import CartItemSerializer, CartItemCreateSerializer, CartUpdateSerializer
from products.models import Product

class CartView(APIView):
    """
    Handle cart operations - get cart contents and add items
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get user's cart contents"""
        cart_items = CartItem.objects.filter(user=request.user).select_related('product', 'product__category')
        serializer = CartItemSerializer(cart_items, many=True)
        
        # Use utility function from core (if created) or keep local logic
        total_amount = sum(item.total_price for item in cart_items)
        
        return Response({
            'items': serializer.data,
            'total_amount': total_amount,
            'item_count': cart_items.count(),
            'currency': 'KES'  # Could come from settings
        })
    
    def post(self, request):
        """Add item to cart or update quantity if exists"""
        serializer = CartItemCreateSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
            
            # Verify product exists and is active
            try:
                product = Product.objects.get(id=product_id, is_active=True)
            except Product.DoesNotExist:
                return Response(
                    {'error': 'Product not found or inactive'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Check stock availability
            if quantity > product.stock:
                return Response(
                    {'error': f'Only {product.stock} items available in stock'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if item already in cart
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                # Update quantity if item already exists
                new_quantity = cart_item.quantity + quantity
                if new_quantity > product.stock:
                    return Response(
                        {'error': f'Cannot add {quantity} items. Only {product.stock - cart_item.quantity} more available'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                cart_item.quantity = new_quantity
                cart_item.save()
            
            return Response(
                {
                    'message': 'Item added to cart successfully',
                    'item': CartItemSerializer(cart_item).data
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handle individual cart item operations - get, update, delete
    """
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).select_related('product')
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CartUpdateSerializer  # Separate serializer for updates
        return CartItemSerializer
    
    def perform_update(self, serializer):
        """Custom update logic with stock validation"""
        cart_item = self.get_object()
        new_quantity = serializer.validated_data.get('quantity', cart_item.quantity)
        
        # Validate stock availability
        if new_quantity > cart_item.product.stock:
            from rest_framework.exceptions import ValidationError
            raise ValidationError(
                f'Only {cart_item.product.stock} items available in stock'
            )
        
        # Validate minimum quantity
        if new_quantity < 1:
            raise ValidationError('Quantity must be at least 1')
        
        serializer.save()
    
    def perform_destroy(self, instance):
        """Custom delete logic with logging"""
        product_name = instance.product.name
        instance.delete()
        
        # Could add logging here
        # logger.info(f"User {self.request.user.email} removed {product_name} from cart")

class CartSummaryView(APIView):
    """
    Get cart summary without full item details
    Useful for header cart count, etc.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        
        total_amount = sum(item.total_price for item in cart_items)
        item_count = cart_items.count()
        total_items = sum(item.quantity for item in cart_items)
        
        return Response({
            'item_count': item_count,  # Unique products
            'total_items': total_items,  # Total quantity
            'total_amount': total_amount,
            'currency': 'KES'
        })

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def clear_cart(request):
    """Clear all items from user's cart"""
    cart_items = CartItem.objects.filter(user=request.user)
    count = cart_items.count()
    
    if count == 0:
        return Response({
            'message': 'Cart is already empty',
            'items_removed': 0
        })
    
    # Store items for potential logging/analytics
    removed_items = [
        {'product_id': item.product.id, 'product_name': item.product.name, 'quantity': item.quantity}
        for item in cart_items
    ]
    
    cart_items.delete()
    
    return Response({
        'message': f'Cleared {count} items from cart',
        'items_removed': count
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_cart_quantity(request, item_id):
    """
    Quick endpoint to update just the quantity of a cart item
    Alternative to using PATCH on CartItemDetailView
    """
    try:
        cart_item = CartItem.objects.get(id=item_id, user=request.user)
    except CartItem.DoesNotExist:
        return Response(
            {'error': 'Cart item not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    quantity = request.data.get('quantity')
    if not quantity or quantity < 1:
        return Response(
            {'error': 'Quantity must be a positive integer'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check stock availability
    if quantity > cart_item.product.stock:
        return Response(
            {'error': f'Only {cart_item.product.stock} items available in stock'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    cart_item.quantity = quantity
    cart_item.save()
    
    return Response({
        'message': 'Cart item updated successfully',
        'item': CartItemSerializer(cart_item).data
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def move_to_favorites(request, item_id):
    """
    Move item from cart to favorites
    Cross-app functionality - could be in core if needed frequently
    """
    try:
        cart_item = CartItem.objects.get(id=item_id, user=request.user)
    except CartItem.DoesNotExist:
        return Response(
            {'error': 'Cart item not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Import here to avoid circular imports
    from favorites.models import Favorite
    
    # Create favorite if doesn't exist
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        product=cart_item.product
    )
    
    # Remove from cart
    product_name = cart_item.product.name
    cart_item.delete()
    
    message = f"Moved {product_name} to favorites"
    if not created:
        message = f"{product_name} was already in favorites. Removed from cart."
    
    return Response({
        'message': message,
        'moved_to_favorites': created
    })