from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('orders/<int:pk>/status/', views.OrderStatusUpdateView.as_view(), name='order-status-update'),
]