from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random

from products.models import Product, Category  
from orders.models import Order  
from reviews.models import Review  
from favorites.models import Favorite

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Seed database with dummy users, products, categories, favorites and orders"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Seeding database..."))

        # === Users ===
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@example.com",
                password="admin123",
                role="admin"
            )
            self.stdout.write(self.style.SUCCESS("Created admin user"))

        for i in range(3):
            username = f"customer{i+1}"
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username,
                    email=f"{username}@example.com",
                    password="password123",
                    role="customer"
                )
        self.stdout.write(self.style.SUCCESS("Created customers"))

        # === Categories ===
        categories = []
        for name in ["Electronics", "Fashion", "Home", "Books"]:
            cat, created = Category.objects.get_or_create(name=name)
            categories.append(cat)
        self.stdout.write(self.style.SUCCESS("Created categories"))

        # === Products ===
        for _ in range(10):
            Product.objects.create(
                name=fake.word().capitalize(),
                description=fake.text(),
                price=round(random.uniform(10, 500), 2),
                stock=random.randint(1, 50),
                category=random.choice(categories)
            )
        self.stdout.write(self.style.SUCCESS("Created products"))

        # === Orders (Optional) ===
        customers = User.objects.filter(role="customer")
        products = Product.objects.all()
        for customer in customers:
            for _ in range(2):
                product = random.choice(products)
                Order.objects.create(
                    customer=customer,
                    product=product,
                    quantity=random.randint(1, 3),
                    total_price=product.price
                )
        self.stdout.write(self.style.SUCCESS("Created orders"))

        # === Reviews (Optional) ===
        for customer in customers:
            for product in products[:5]:
                Review.objects.create(
                    customer=customer,
                    product=product,
                    rating=random.randint(3, 5),
                    comment=fake.sentence()
                )
        self.stdout.write(self.style.SUCCESS("Created reviews"))

        self.stdout.write(self.style.SUCCESS("✅ Seeding complete!"))
