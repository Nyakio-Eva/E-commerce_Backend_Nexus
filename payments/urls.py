from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('payments/initiate/', views.PaymentInitiateView.as_view(), name='payment-initiate'),
    path('payments/verify/', views.PaymentVerifyView.as_view(), name='payment-verify'),
    path('payments/history/', views.PaymentHistoryView.as_view(), name='payment-history'),
]
