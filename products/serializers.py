from rest_framework import serializers
from products.models import Product, Category


# Category Serializers
class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'product_count', 'created_at', 'updated_at')

    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'description')

# Product Serializers
class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'price', 'image_url', 'image_alt', 
            'rating', 'stock', 'category_name', 'is_in_stock'
        )

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'description', 'price', 'image_url', 'image_alt',
            'rating', 'stock', 'sku', 'category', 'review_count', 
            'is_in_stock', 'created_at', 'updated_at'
        )

    def get_review_count(self, obj):
        return obj.reviews.count()

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name', 'description', 'price', 'image_url', 'image_alt',
            'stock', 'sku', 'category', 'is_active'
        )

    def validate_sku(self, value):
        instance = getattr(self, 'instance', None)
        if Product.objects.filter(sku=value).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError("Product with this SKU already exists.")
        return value
