# models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    """Custom manager for User model with email as the unique identifier."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        # Generate username from email if not provided
        if not extra_fields.get('username'):
            extra_fields['username'] = email.split('@')[0]
            
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
            
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Role choices
    CUSTOMER = 'customer'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (ADMIN, 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CUSTOMER)

    # Use email as the unique identifier for authentication
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Remove username from required fields
    
    # Use custom manager
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    class Meta:
        db_table = 'auth_user'  # keeps the same table name
        verbose_name = 'User'
        verbose_name_plural = 'Users'