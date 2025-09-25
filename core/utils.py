# Utility functions
import uuid
from decimal import Decimal
from django.core.mail import send_mail
from django.conf import settings

def generate_order_number():
    """Generate unique order number"""
    return f"ORD-{uuid.uuid4().hex[:8].upper()}"

def generate_transaction_id(payment_method):
    """Generate unique transaction ID"""
    return f"{payment_method.upper()}-{uuid.uuid4().hex[:12]}"

def send_order_confirmation_email(order):
    """Send order confirmation email"""
    subject = f"Order Confirmation - {order.order_number}"
    message = f"""
    Dear {order.user.email},
    
    Your order {order.order_number} has been confirmed.
    Total Amount: ${order.total_amount}
    
    Thank you for shopping with us!
    """
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [order.user.email],
        fail_silently=False,
    )

def calculate_cart_total(cart_items):
    """Calculate total for cart items"""
    return sum(item.total_price for item in cart_items)