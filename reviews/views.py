from django.shortcuts import render
from rest_framework import generics, permissions

from django.shortcuts import get_object_or_404

# Import shared functionality from core
# from core.pagination import StandardResultsSetPagination
from core.permissions import IsOwnerOrReadOnly

# Local app imports
from products.models import Product
from .models import Review
from .serializers import (
    ReviewSerializer,
    ReviewCreateUpdateSerializer, 
    
)

# Create your views here.
class ProductReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return Review.objects.filter(product_id=product_id)
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateUpdateSerializer
        return ReviewSerializer
    
    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        # Check if user has already reviewed this product
        if Review.objects.filter(user=self.request.user, product=product).exists():
            raise serializer.ValidationError("You have already reviewed this product.")
        
        review = serializer.save(user=self.request.user, product=product)
        
        # Update product rating
        product.update_rating()

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewCreateUpdateSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
    
    def perform_update(self, serializer):
        review = serializer.save()
        # Update product rating after review update
        review.product.update_rating()
    
    def perform_destroy(self, instance):
        product = instance.product
        instance.delete()
        # Update product rating after review deletion
        product.update_rating()
