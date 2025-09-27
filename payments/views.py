from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

import uuid

from .models import  Payment
from orders.models import Order
from .serializers import (
    PaymentSerializer, PaymentInitiateSerializer, PaymentVerifySerializer
)
from core.pagination import StandardResultsSetPagination

# Create your views here.
class PaymentInitiateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PaymentInitiateSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            order_id = serializer.validated_data['order_id']
            payment_method = serializer.validated_data['payment_method']
            
            order = get_object_or_404(Order, id=order_id, user=request.user)
            
            # Generate unique transaction ID
            transaction_id = f"{payment_method.upper()}-{uuid.uuid4().hex[:12]}"
            
            # Create payment record
            payment = Payment.objects.create(
                order=order,
                amount=order.total_amount,
                method=payment_method,
                transaction_id=transaction_id
            )
            
            # integrate with actual payment gateways
            # For demo purposes, we'll return mock payment data
            
            response_data = {
                'transaction_id': transaction_id,
                'amount': order.total_amount,
                'payment_method': payment_method,
                'status': 'pending',
                'payment_url': f'https://payment-gateway.com/pay/{transaction_id}'  # Mock URL
            }
            
            if payment_method == Payment.MPESA:
                response_data.update({
                    'checkout_request_id': f"ws_CO_{uuid.uuid4().hex[:20]}",
                    'merchant_request_id': f"mr_{uuid.uuid4().hex[:15]}"
                })
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentVerifyView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PaymentVerifySerializer(data=request.data)
        
        if serializer.is_valid():
            transaction_id = serializer.validated_data['transaction_id']
            payment_method = serializer.validated_data['payment_method']
            
            try:
                payment = Payment.objects.get(
                    transaction_id=transaction_id,
                    method=payment_method,
                    order__user=request.user
                )
                
                # Here you would verify with actual payment gateway
                # For demo purposes, we'll mark as completed
                payment.status = Payment.COMPLETED
                payment.save()
                
                # Update order status
                payment.order.status = Order.CONFIRMED
                payment.order.save()
                
                return Response({
                    'message': 'Payment verified successfully',
                    'payment_status': payment.status,
                    'order_status': payment.order.status
                })
                
            except Payment.DoesNotExist:
                return Response(
                    {'error': 'Payment not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentHistoryView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        return Payment.objects.filter(order__user=self.request.user)
