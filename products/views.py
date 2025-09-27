# products/views.py
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# Import shared functionality from core
from core.pagination import StandardResultsSetPagination
from core.permissions import IsAdminOrReadOnly

# Local app imports
from .models import Category, Product
from .serializers import (
    CategoryCreateSerializer, 
    CategorySerializer, 
    ProductCreateUpdateSerializer, 
    ProductDetailSerializer, 
    ProductListSerializer
)
from .filters import ProductFilter, CategoryFilter  # If you create these

# Category Views
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination  # Using core pagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CategoryFilter  # create CategoryFilter
    search_fields = ['name', 'description']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryCreateSerializer
        return CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]  # Using core permission
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CategoryCreateSerializer
        return CategorySerializer

# Product Views
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True)
    pagination_class = StandardResultsSetPagination  # Using core pagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter  # Using custom filter class
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['price', 'rating', 'created_at', 'name']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateUpdateSerializer
        return ProductListSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
    # Remove the get_queryset method since filtering is handled by ProductFilter

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(is_active=True)
    permission_classes = [IsAdminOrReadOnly]  # Using core permission
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductCreateUpdateSerializer
        return ProductDetailSerializer

# Additional product-specific views
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def products_by_category(request, category_id):
    """Get products by specific category"""
    try:
        category = Category.objects.get(id=category_id)
        products = Product.objects.filter(category=category, is_active=True)
        
        # Using core pagination
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(products, request)
        
        if page is not None:
            serializer = ProductListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=404)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def product_recommendations(request, product_id):
    """Get recommended products based on category and rating"""
    try:
        product = Product.objects.get(id=product_id, is_active=True)
        
        # Get similar products from same category
        recommendations = Product.objects.filter(
            category=product.category,
            is_active=True,
            rating__gte=3.0
        ).exclude(id=product_id).order_by('-rating', '-created_at')[:6]
        
        serializer = ProductListSerializer(recommendations, many=True)
        return Response({
            'product': ProductDetailSerializer(product).data,
            'recommendations': serializer.data
        })
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

# Admin-specific product views
class LowStockProductsView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    pagination_class = StandardResultsSetPagination  # Using core pagination
    
    def get_queryset(self):
        threshold = self.request.query_params.get('threshold', 10)
        return Product.objects.filter(
            is_active=True,
            stock__lte=threshold
        ).order_by('stock')