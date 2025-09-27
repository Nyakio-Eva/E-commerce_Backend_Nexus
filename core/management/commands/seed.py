from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from faker import Faker
from decimal import Decimal
import random

from products.models import Product, Category
from orders.models import Order, OrderItem
from reviews.models import Review
from cart.models import CartItem
from favorites.models import Favorite

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Seed database with dummy data using Faker"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.clear_data()
        
        self.stdout.write(self.style.WARNING("Seeding database with Faker..."))

        # Create users
        users = self.create_users()
        
        # Create categories  
        categories = self.create_categories()
        
        # Create products
        products = self.create_products(categories)
        
        # Create reviews
        self.create_reviews(users, products)
        
        # Create favorites
        self.create_favorites(users, products)
        
        # Create cart items and orders
        self.create_cart_items_and_orders(users, products)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
        self.print_credentials()

    def clear_data(self):
        """Clear existing data safely"""
        self.stdout.write(self.style.WARNING("Clearing existing data..."))
        
        # Clear data in order to avoid foreign key constraint issues
        models_to_clear = [
            ('Favorite', Favorite),
            ('Review', Review),
            ('OrderItem', OrderItem), 
            ('Order', Order),
            ('CartItem', CartItem),
            ('Product', Product),
            ('Category', Category),
            ('User', User),
        ]
        
        for model_name, model_class in models_to_clear:
            try:
                count = model_class.objects.all().count()
                if count > 0:
                    model_class.objects.all().delete()
                    self.stdout.write(f"   Cleared {count} {model_name} records")
                else:
                    self.stdout.write(f"   No {model_name} records to clear")
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"   Could not clear {model_name}: {e}")
                )
        
        self.stdout.write(self.style.SUCCESS("Data clearing completed"))

    def create_users(self):
        """Create test users with proper field names"""
        self.stdout.write("Creating users...")
        
        users = []
        
        # Admin user - check if exists first
        admin_email = "admin@geocel.com"
        admin_user = User.objects.filter(email=admin_email).first()
        
        if not admin_user:
            try:
                admin_user = User.objects.create_superuser(
                    email=admin_email,
                    password="admin123",
                    role="admin"
                )
                self.stdout.write(self.style.SUCCESS("Created admin user"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Admin user creation failed: {e}"))
                # Try to get existing admin user
                admin_user = User.objects.filter(is_superuser=True).first()
        else:
            self.stdout.write(self.style.WARNING("Admin user already exists"))
        
        if admin_user:
            users.append(admin_user)

        # Regular customers with Faker data
        for i in range(5):
            email = fake.unique.email()
            
            if not User.objects.filter(email=email).exists():
                try:
                    customer = User.objects.create_user(
                        email=email,
                        password="customer123",
                        role="customer"
                    )
                    users.append(customer)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Failed to create customer {email}: {e}"))
        
        self.stdout.write(self.style.SUCCESS(f"Using {len(users)} users"))
        return users

    def create_categories(self):
        """Create product categories"""
        self.stdout.write("Creating categories...")
        
        category_data = [
            {
                'name': 'Electronics',
                'description': 'Electronic devices, gadgets, and tech accessories'
            },
            {
                'name': 'Fashion & Clothing', 
                'description': 'Apparel, shoes, and fashion accessories'
            },
            {
                'name': 'Home & Living',
                'description': 'Home improvement, furniture, and living essentials'
            },
            {
                'name': 'Sports & Fitness',
                'description': 'Sports equipment, fitness gear, and outdoor activities'
            },
            {
                'name': 'Books & Education',
                'description': 'Books, educational materials, and learning resources'
            },
            {
                'name': 'Beauty & Personal Care',
                'description': 'Beauty products, skincare, and personal care items'
            },
            {
                'name': 'Automotive',
                'description': 'Car accessories, parts, and automotive supplies'
            },
            {
                'name': 'Food & Beverages',
                'description': 'Gourmet foods, beverages, and cooking ingredients'
            }
        ]
        
        categories = []
        for data in category_data:
            category, created = Category.objects.get_or_create(
                name=data['name'],
                defaults={'description': data['description']}
            )
            categories.append(category)
        
        self.stdout.write(self.style.SUCCESS(f"Created {len(categories)} categories"))
        return categories

    def create_products(self, categories):
        """Create products with Faker data"""
        self.stdout.write("Creating products...")
        
        products = []
        
        # Product name templates by category
        product_templates = {
            'Electronics': [
                'Smartphone', 'Laptop', 'Headphones', 'Smart Watch', 'Tablet',
                'Camera', 'Gaming Console', 'Bluetooth Speaker', 'Monitor', 'Keyboard'
            ],
            'Fashion & Clothing': [
                'Sneakers', 'Jeans', 'T-Shirt', 'Dress', 'Jacket',
                'Hoodie', 'Boots', 'Backpack', 'Sunglasses', 'Watch'
            ],
            'Home & Living': [
                'Coffee Maker', 'Vacuum Cleaner', 'Air Purifier', 'Lamp', 'Pillow',
                'Blanket', 'Storage Box', 'Picture Frame', 'Candle', 'Plant Pot'
            ],
            'Sports & Fitness': [
                'Yoga Mat', 'Dumbbells', 'Running Shoes', 'Fitness Tracker', 'Water Bottle',
                'Resistance Bands', 'Basketball', 'Tennis Racket', 'Gym Bag', 'Protein Powder'
            ],
            'Books & Education': [
                'Fiction Novel', 'Self-Help Book', 'Cookbook', 'Textbook', 'Notebook',
                'Art Supplies', 'Calculator', 'Dictionary', 'Magazine', 'Journal'
            ],
            'Beauty & Personal Care': [
                'Face Moisturizer', 'Shampoo', 'Lipstick', 'Perfume', 'Sunscreen',
                'Face Mask', 'Hair Serum', 'Body Lotion', 'Toothbrush', 'Nail Polish'
            ],
            'Automotive': [
                'Car Charger', 'Phone Mount', 'Air Freshener', 'Tire Gauge', 'Jump Starter',
                'Dashboard Camera', 'Seat Covers', 'Floor Mats', 'Tool Kit', 'Car Wax'
            ],
            'Food & Beverages': [
                'Organic Coffee', 'Green Tea', 'Protein Bar', 'Olive Oil', 'Honey',
                'Dark Chocolate', 'Nuts Mix', 'Energy Drink', 'Spice Set', 'Pasta'
            ]
        }
        
        for category in categories:
            # Get templates for this category or use generic ones
            templates = product_templates.get(category.name, ['Product'])
            
            # Create 8-12 products per category
            for i in range(random.randint(8, 12)):
                template = random.choice(templates)
                brand = fake.company().split()[0]  # Get first word of company name as brand
                
                # Create realistic product data
                product_data = {
                    'name': f"{brand} {template} {fake.word().capitalize()}",
                    'description': fake.text(max_nb_chars=200),
                    'price': Decimal(str(round(random.uniform(9.99, 999.99), 2))),
                    'stock': random.randint(0, 100),
                    'category': category,  # This should match your model's field name
                    'rating': round(random.uniform(3.0, 5.0), 1),
                }
                
                
                if hasattr(Product, 'sku'):
                    product_data['sku'] = fake.unique.ean13()
                if hasattr(Product, 'image_url'):
                    product_data['image_url'] = fake.image_url()
                if hasattr(Product, 'is_active'):
                    product_data['is_active'] = True
                
                try:
                    product = Product.objects.create(**product_data)
                    products.append(product)
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error creating product: {e}")
                    )
        
        self.stdout.write(self.style.SUCCESS(f"Created {len(products)} products"))
        return products

    def create_reviews(self, users, products):
        """Create product reviews"""
        self.stdout.write("Creating reviews...")
        
        reviews = []
        customers = [user for user in users if getattr(user, 'role', None) == 'customer']
        
        for customer in customers:
            # Each customer reviews 3-7 random products
            reviewed_products = random.sample(
                products, 
                min(random.randint(3, 7), len(products))
            )
            
            for product in reviewed_products:
                # Check field names for Review model
                review_data = {
                    'user': customer,  # or 'customer': customer if that's your field name
                    'product': product,
                    'rating': random.randint(3, 5),
                    'comment': fake.sentence(nb_words=random.randint(10, 30)),
                }
                
                try:
                    review = Review.objects.create(**review_data)
                    reviews.append(review)
                except Exception as e:
                    # Try alternative field name
                    if 'user' in str(e):
                        review_data['customer'] = review_data.pop('user')
                        try:
                            review = Review.objects.create(**review_data)
                            reviews.append(review)
                        except Exception as e2:
                            self.stdout.write(
                                self.style.ERROR(f"Error creating review: {e2}")
                            )
        
        self.stdout.write(self.style.SUCCESS(f"Created {len(reviews)} reviews"))
        return reviews

    def create_favorites(self, users, products):
        """Create user favorites"""
        self.stdout.write("Creating favorites...")
        
        favorites = []
        customers = [user for user in users if getattr(user, 'role', None) == 'customer']
        
        for customer in customers:
            # Each customer favorites 2-5 random products
            favorite_products = random.sample(
                products, 
                min(random.randint(2, 5), len(products))
            )
            
            for product in favorite_products:
                # Check field names for Favorite model
                favorite_data = {
                    'user': customer,  # or 'customer': customer if that's your field name
                    'product': product,
                }
                
                try:
                    favorite, created = Favorite.objects.get_or_create(**favorite_data)
                    if created:
                        favorites.append(favorite)
                except Exception as e:
                    # Try alternative field name
                    if 'user' in str(e):
                        favorite_data['customer'] = favorite_data.pop('user')
                        try:
                            favorite, created = Favorite.objects.get_or_create(**favorite_data)
                            if created:
                                favorites.append(favorite)
                        except Exception as e2:
                            self.stdout.write(
                                self.style.ERROR(f"Error creating favorite: {e2}")
                            )
        
        self.stdout.write(self.style.SUCCESS(f"Created {len(favorites)} favorites"))
        return favorites

    def create_cart_items_and_orders(self, users, products):
        """Create cart items and orders"""
        self.stdout.write("Creating cart items and orders...")
        
        customers = [user for user in users if getattr(user, 'role', None) == 'customer']
        orders = []
        cart_items = []
        
        for customer in customers:
            # Create cart items directly for each customer
            # Note: This assumes your CartItem model has a user field
            # If it only has a cart field, you'll need to adjust this
            cart_products = random.sample(products, random.randint(1, 4))
            for product in cart_products:
                try:
                    cart_item_data = {
                        'user': customer,  # Adjust field name based on your model
                        'product': product,
                        'quantity': random.randint(1, 3)
                    }
                    
                    cart_item = CartItem.objects.create(**cart_item_data)
                    cart_items.append(cart_item)
                    
                except Exception as e:
                    # Try alternative field name if 'user' doesn't work
                    if 'user' in str(e):
                        cart_item_data['customer'] = cart_item_data.pop('user')
                        try:
                            cart_item = CartItem.objects.create(**cart_item_data)
                            cart_items.append(cart_item)
                        except Exception as e2:
                            self.stdout.write(
                                self.style.ERROR(f"Error creating cart item: {e2}")
                            )
            
            # Create 1-3 historical orders for each customer
            for _ in range(random.randint(1, 3)):
                order_products = random.sample(products, random.randint(1, 4))
                total_amount = Decimal('0.00')
                
                # Calculate total amount
                order_items_data = []
                for product in order_products:
                    quantity = random.randint(1, 3)
                    item_total = product.price * quantity
                    total_amount += item_total
                    order_items_data.append({
                        'product': product,
                        'quantity': quantity,
                        'price': product.price
                    })
                
                # Create order - check your Order model field names
                order_data = {
                    'user': customer,  # or 'customer': customer if that's your field
                    'total_amount': total_amount,
                    'status': random.choice(['pending', 'processing', 'shipped', 'delivered']),
                    'created_at': fake.date_time_between(start_date='-60d', end_date='now', tzinfo=timezone.get_current_timezone())
                }
                
                try:
                    order = Order.objects.create(**order_data)
                    
                    # Create order items
                    for item_data in order_items_data:
                        OrderItem.objects.create(
                            order=order,
                            product=item_data['product'],
                            quantity=item_data['quantity'],
                            price=item_data['price']
                        )
                    
                    orders.append(order)
                    
                except Exception as e:
                    # Try alternative field name
                    if 'user' in str(e):
                        order_data['customer'] = order_data.pop('user')
                        try:
                            order = Order.objects.create(**order_data)
                            orders.append(order)
                        except Exception as e2:
                            self.stdout.write(
                                self.style.ERROR(f"Error creating order: {e2}")
                            )
        
        self.stdout.write(self.style.SUCCESS(f"Created {len(cart_items)} cart items"))
        self.stdout.write(self.style.SUCCESS(f"Created {len(orders)} orders"))
        return orders

    def print_credentials(self):
        """Print test credentials"""
        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS("Test Credentials:"))
        self.stdout.write("   Admin: admin@geocel.com / admin123")
        self.stdout.write("   Customers: Use any generated email / customer123")
        self.stdout.write("\n Summary:")
        self.stdout.write(f"   - Users: {User.objects.count()}")
        self.stdout.write(f"   - Categories: {Category.objects.count()}")
        self.stdout.write(f"   - Products: {Product.objects.count()}")
        self.stdout.write(f"   - Reviews: {Review.objects.count()}")
        self.stdout.write(f"   - Favorites: {Favorite.objects.count()}")
        self.stdout.write(f"   - Cart Items: {CartItem.objects.count()}")
        self.stdout.write(f"   - Orders: {Order.objects.count()}")
        self.stdout.write("="*50)