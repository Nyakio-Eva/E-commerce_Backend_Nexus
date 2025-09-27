from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User 
from products.models import Product

# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.product.name} ({self.quantity})"

    @property
    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        unique_together = ('user', 'product')