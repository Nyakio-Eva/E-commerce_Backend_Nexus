import django_filters
from django_filters import rest_framework as filters
from .models import Order

class OrderFilter(filters.FilterSet):
    """Order-specific filtering logic"""
    status = filters.ChoiceFilter(choices=Order.STATUS_CHOICES)
    date_from = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='created_at', lookup_expr='lte')
    min_amount = filters.NumberFilter(field_name='total_amount', lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name='total_amount', lookup_expr='lte')
    user_email = filters.CharFilter(field_name='user__email', lookup_expr='icontains')
    
    class Meta:
        model = Order
        fields = ['status', 'user']