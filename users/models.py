# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

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

    def __str__(self):
        return self.email
    
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    class Meta:
        db_table = 'auth_user'  #keeps the same table name
        verbose_name = 'User'
        verbose_name_plural = 'Users'