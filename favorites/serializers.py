from rest_framework import serializers
from products.serializers import ProductListSerializer
from favorites.models import Favorite
from products.models import Product

class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'product', 'created_at')

class FavoriteCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = Favorite
        fields = ('product_id',)

    def validate_product_id(self, value):
        try:
            Product.objects.get(id=value, is_active=True)
            return value
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found.")

