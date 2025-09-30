from django.urls import path
from .views import (
    RegisterView, LoginView, ProfileView,
    ChangePasswordView, ResetPasswordView,
    AdminDashboardView, AdminUserListView,
    AdminOrderListView, LowStockProductsView,
    verify_email, resend_verification_email,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    # Email verification endpoints
    path('verify-email/', verify_email, name='verify-email'),
    path('resend-verification/', resend_verification_email, name='resend-verification'),
    
    #admin urls
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('admin/users/', AdminUserListView.as_view(), name='admin-users'),
    path('admin/orders/', AdminOrderListView.as_view(), name='admin-orders'),
    path('admin/products/low-stock/', LowStockProductsView.as_view(), name='low-stock-products'),
]
