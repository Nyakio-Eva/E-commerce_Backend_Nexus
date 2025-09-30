from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import EmailVerificationToken

def send_verification_email(user, request=None):
    """
    Generate a verification token and send verification email to the user
    """
    # Create verification token
    token = EmailVerificationToken.objects.create(user=user)
    
    # Build verification URL (adjust based on your frontend)
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token.token}"
    
    # Email context
    context = {
        'user': user,
        'verification_url': verification_url,
        'site_name': 'Geocel Enterprises',
    }
    
    # Render email template
    html_message = render_to_string('emails/verification_email.html', context)
    plain_message = strip_tags(html_message)
    
    # Send email
    send_mail(
        subject='Verify your email address',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )