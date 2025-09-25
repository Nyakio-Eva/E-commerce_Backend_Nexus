from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Main cart operations
    path('', views.CartView.as_view(), name='cart'),
    path('summary/', views.CartSummaryView.as_view(), name='cart-summary'),
    
    # Individual cart item operations
    path('items/<int:pk>/', views.CartItemDetailView.as_view(), name='cart-item-detail'),
    path('items/<int:item_id>/quantity/', views.update_cart_quantity, name='update-quantity'),
    
    # Bulk operations
    path('clear/', views.clear_cart, name='clear-cart'),
    
    # Cross-app functionality
    path('items/<int:item_id>/move-to-favorites/', views.move_to_favorites, name='move-to-favorites'),
]