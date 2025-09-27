from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('initiate/', views.PaymentInitiateView.as_view(), name='payment-initiate'),
    path('verify/', views.PaymentVerifyView.as_view(), name='payment-verify'),
    path('history/', views.PaymentHistoryView.as_view(), name='payment-history'),
]
