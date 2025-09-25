
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Category endpoints
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # Product endpoints
    path('', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    
    # Additional product endpoints
    path('categories/<int:category_id>/products/', views.products_by_category, name='products-by-category'),
    # path('<int:product_id>/recommendations/', views.product_recommendations, name='product-recommendations'),
    
    # Admin endpoints
    path('low-stock/', views.LowStockProductsView.as_view(), name='low-stock-products'),
]