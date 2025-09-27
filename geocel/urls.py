"""
URL configuration for geocel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# API URL patterns
api_patterns = [
    # Authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # App endpoints
    path('users/', include('users.urls')),  # Register/Login endpoints
    path('products/', include('products.urls')),  # products/categories endpoints
    path('cart/', include('cart.urls', namespace='cart')),  # cart and cart items
    path('favorites/', include('favorites.urls', namespace='favorites')),  # wishlist endpoints
    path('orders/', include('orders.urls')),  # orders endpoints
    path('reviews/', include('reviews.urls')),  # reviews
    path('payments/', include('payments.urls')),  # payments
]

# Main URL patterns
urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include(api_patterns)),
    
    # API Documentation endpoints
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Root endpoint redirect to documentation
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='api-docs'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Add debug toolbar in development
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass