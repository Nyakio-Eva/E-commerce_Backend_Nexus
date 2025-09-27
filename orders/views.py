from django.shortcuts import render
from rest_framework import generics, permissions


# Import shared functionality from core
from core.pagination import StandardResultsSetPagination
from core.permissions import IsAdminOrReadOnly

# Local app imports
from .models import Order
from .serializers import (
    OrderSerializer,
    OrderStatusUpdateSerializer, 
    OrderCreateSerializer, 
    
)
from .filters import OrderFilter

# Create your views here.
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class CheckoutView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderStatusUpdateView(generics.UpdateAPIView):
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = Order.objects.all()
    http_method_names = ['patch']
