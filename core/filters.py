# core/filters.py
import django_filters
from django_filters import rest_framework as filters
from django.db.models import Q

class DateRangeFilterMixin:
    """
    Mixin for common date range filtering
    Provides created_from, created_to, updated_from, updated_to filters
    """
    created_from = filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte',
        help_text="Filter records created after this date (YYYY-MM-DD HH:MM:SS)"
    )
    created_to = filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte',
        help_text="Filter records created before this date (YYYY-MM-DD HH:MM:SS)"
    )
    updated_from = filters.DateTimeFilter(
        field_name='updated_at',
        lookup_expr='gte',
        help_text="Filter records updated after this date (YYYY-MM-DD HH:MM:SS)"
    )
    updated_to = filters.DateTimeFilter(
        field_name='updated_at',
        lookup_expr='lte',
        help_text="Filter records updated before this date (YYYY-MM-DD HH:MM:SS)"
    )

class PriceRangeFilterMixin:
    """
    Mixin for price range filtering
    Provides min_price and max_price filters
    """
    min_price = filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        help_text="Minimum price"
    )
    max_price = filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        help_text="Maximum price"
    )
    price_exact = filters.NumberFilter(
        field_name='price',
        lookup_expr='exact',
        help_text="Exact price match"
    )

class SearchFilterMixin:
    """
    Mixin for text search functionality
    Subclasses must implement filter_search method
    """
    q = filters.CharFilter(
        method='filter_search',
        help_text="Search query - searches across multiple fields"
    )
    search = filters.CharFilter(
        method='filter_search',
        help_text="Alias for 'q' parameter"
    )
    
    def filter_search(self, queryset, name, value):
        """
        Override this method in subclasses to define search fields
        Example:
        return queryset.filter(
            Q(name__icontains=value) | Q(description__icontains=value)
        )
        """
        raise NotImplementedError(
            "Subclass must implement filter_search method to define searchable fields"
        )

class ActiveFilterMixin:
    """
    Mixin for filtering active/inactive records
    """
    is_active = filters.BooleanFilter(
        field_name='is_active',
        help_text="Filter by active status"
    )
    active_only = filters.BooleanFilter(
        method='filter_active_only',
        help_text="Show only active records"
    )
    
    def filter_active_only(self, queryset, name, value):
        """Filter to show only active records"""
        if value:
            return queryset.filter(is_active=True)
        return queryset

class UserFilterMixin:
    """
    Mixin for filtering records by user
    Useful for user-owned resources
    """
    user_email = filters.CharFilter(
        field_name='user__email',
        lookup_expr='icontains',
        help_text="Filter by user email"
    )
    user_id = filters.NumberFilter(
        field_name='user__id',
        help_text="Filter by user ID"
    )

class OrderingFilterMixin:
    """
    Mixin that provides common ordering options
    Note: This is more of a reference - actual ordering is handled in views
    """
    # This is informational - actual ordering is set in view's ordering_fields
    COMMON_ORDERING_FIELDS = [
        'created_at', '-created_at',
        'updated_at', '-updated_at',
        'name', '-name'
    ]

# Utility functions for complex filtering
def apply_user_permissions(queryset, user, user_field='user'):
    """
    Apply user-based filtering based on permissions
    Args:
        queryset: QuerySet to filter
        user: User instance
        user_field: Field name that relates to user (default: 'user')
    """
    if not user.is_authenticated:
        return queryset.none()
    
    if user.is_admin():
        return queryset  # Admin sees everything
    
    # Regular users see only their own records
    filter_kwargs = {user_field: user}
    return queryset.filter(**filter_kwargs)

def apply_date_range_filter(queryset, field_name, start_date, end_date):
    """
    Utility function to apply date range filtering
    Args:
        queryset: QuerySet to filter
        field_name: Date field name to filter on
        start_date: Start date (inclusive)
        end_date: End date (inclusive)
    """
    if start_date:
        filter_kwargs = {f"{field_name}__gte": start_date}
        queryset = queryset.filter(**filter_kwargs)
    
    if end_date:
        filter_kwargs = {f"{field_name}__lte": end_date}
        queryset = queryset.filter(**filter_kwargs)
    
    return queryset

def apply_text_search(queryset, search_value, search_fields):
    """
    Utility function to apply text search across multiple fields
    Args:
        queryset: QuerySet to filter
        search_value: Text to search for
        search_fields: List of field names to search in
    """
    if not search_value:
        return queryset
    
    query = Q()
    for field in search_fields:
        query |= Q(**{f"{field}__icontains": search_value})
    
    return queryset.filter(query)

# Base filter class that combines common mixins
class BaseFilter(DateRangeFilterMixin, ActiveFilterMixin, SearchFilterMixin, filters.FilterSet):
    """
    Base filter class that includes most common filtering patterns
    Inherit from this for standard CRUD resources
    """
    
    def filter_search(self, queryset, name, value):
        """
        Default search implementation - searches 'name' field
        Override in subclasses for more specific search logic
        """
        if hasattr(queryset.model, 'name'):
            return queryset.filter(name__icontains=value)
        return queryset