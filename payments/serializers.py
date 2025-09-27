from rest_framework import serializers
from payments.models import Payment
from orders.models import Order


class PaymentSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='order.order_number', read_only=True)

    class Meta:
        model = Payment
        fields = (
            'id', 'order_number', 'amount', 'method', 'status',
            'transaction_id', 'created_at', 'updated_at'
        )

class PaymentInitiateSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(choices=Payment.METHOD_CHOICES)

    def validate_order_id(self, value):
        user = self.context['request'].user
        try:
            order = Order.objects.get(id=value, user=user)
            if hasattr(order, 'payment'):
                raise serializers.ValidationError("Payment already exists for this order.")
            return value
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order not found.")

class PaymentVerifySerializer(serializers.Serializer):
    transaction_id = serializers.CharField()
    payment_method = serializers.ChoiceField(choices=Payment.METHOD_CHOICES)