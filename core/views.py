from django.shortcuts import render

# Create your views here.
# Utility views (health check, search, etc.)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status
from django.db.models import Q
from products.models import Product
from products.serializers import ProductListSerializer
from .pagination import StandardResultsSetPagination

@api_view(['GET'])
def health_check(request):
    """Simple health check endpoint"""
    return Response({
        'status': 'healthy',
        'message': 'E-commerce API is running'
    })

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def global_search(request):
    """Global search across products"""
    query = request.query_params.get('q', '')
    if not query:
        return Response({'error': 'Query parameter required'}, status=400)
    
    products = Product.objects.filter(
        Q(name__icontains=query) | 
        Q(description__icontains=query),
        is_active=True
    )
    
    paginator = StandardResultsSetPagination()
    page = paginator.paginate_queryset(products, request)
    
    if page is not None:
        serializer = ProductListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_products(request):
    """Get featured products (highest rated)"""
    products = Product.objects.filter(
        is_active=True,
        rating__gte=4.0
    ).order_by('-rating', '-created_at')[:12]
    
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)