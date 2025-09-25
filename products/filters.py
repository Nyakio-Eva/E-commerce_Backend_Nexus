import django_filters
from django_filters import rest_framework as filters
from django.db.models import Q

# Import core filter mixins
from core.filters import DateRangeFilterMixin, PriceRangeFilterMixin, SearchFilterMixin

from .models import Product, Category

class ProductFilter(DateRangeFilterMixin, PriceRangeFilterMixin, SearchFilterMixin, filters.FilterSet):
    """
    Product filtering with inherited common patterns from core
    """
    # Product-specific filters
    category = filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        help_text="Filter by category ID"
    )
    category_name = filters.CharFilter(
        field_name='category__name',
        lookup_expr='icontains',
        help_text="Filter by category name"
    )
    
    # Stock filters
    in_stock = filters.BooleanFilter(
        method='filter_in_stock',
        help_text="Filter by stock availability"
    )
    low_stock = filters.BooleanFilter(
        method='filter_low_stock',
        help_text="Filter products with low stock (≤10)"
    )
    min_stock = filters.NumberFilter(
        field_name='stock',
        lookup_expr='gte',
        help_text="Minimum stock quantity"
    )
    
    # Rating filters
    min_rating = filters.NumberFilter(
        field_name='rating',
        lookup_expr='gte',
        help_text="Minimum rating (0-5)"
    )
    featured = filters.BooleanFilter(
        method='filter_featured',
        help_text="Filter highly rated products (≥4.0)"
    )
    
    # Text search
    sku = filters.CharFilter(
        lookup_expr='icontains',
        help_text="Search by SKU"
    )
    
    class Meta:
        model = Product
        fields = {
            'is_active': ['exact'],
            'price': ['exact', 'gte', 'lte'],
            'rating': ['exact', 'gte', 'lte'],
            'stock': ['exact', 'gte', 'lte'],
        }
    
    def filter_search(self, queryset, name, value):
        """
        Override from SearchFilterMixin to define product search fields
        """
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value) |
            Q(sku__icontains=value) |
            Q(category__name__icontains=value)
        )
    
    def filter_in_stock(self, queryset, name, value):
        """Filter products based on stock availability"""
        if value:
            return queryset.filter(stock__gt=0)
        return queryset.filter(stock=0)
    
    def filter_low_stock(self, queryset, name, value):
        """Filter products with low stock"""
        if value:
            return queryset.filter(stock__lte=10, stock__gt=0)
        return queryset
    
    def filter_featured(self, queryset, name, value):
        """Filter featured/highly-rated products"""
        if value:
            return queryset.filter(rating__gte=4.0)
        return queryset

class CategoryFilter(DateRangeFilterMixin, SearchFilterMixin, filters.FilterSet):
    """
    Category filtering with inherited common patterns
    """
    has_products = filters.BooleanFilter(
        method='filter_has_products',
        help_text="Filter categories that have products"
    )
    min_products = filters.NumberFilter(
        method='filter_min_products',
        help_text="Filter categories with minimum number of products"
    )
    
    class Meta:
        model = Category
        fields = {
            'name': ['exact', 'icontains'],
        }
    
    def filter_search(self, queryset, name, value):
        """
        Override from SearchFilterMixin for category search
        """
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value)
        )
    
    def filter_has_products(self, queryset, name, value):
        """Filter categories that have active products"""
        if value:
            return queryset.filter(products__is_active=True).distinct()
        return queryset.filter(products__isnull=True)
    
    def filter_min_products(self, queryset, name, value):
        """Filter categories with minimum number of products"""
        from django.db.models import Count
        return queryset.annotate(
            product_count=Count('products', filter=Q(products__is_active=True))
        ).filter(product_count__gte=value)