from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'order_number', 'order_status', 'subtotal', 'shipping_cost',
            'tax_amount', 'discount_amount', 'grand_total', 'coupon', 'shipping_address',
            'billing_address', 'payment_method', 'payment_status', 'notes', 'ordered_at', 'items'
        ]
        read_only_fields = ['id', 'order_number', 'ordered_at']


class OrderCreateSerializer(serializers.Serializer):
    shipping_address_id = serializers.IntegerField()
    billing_address_id = serializers.IntegerField(required=False, allow_null=True)
    payment_method = serializers.ChoiceField(choices=[
        ('cod', 'Cash On Delivery'),
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('jazzcash', 'JazzCash'),
        ('easypaisa', 'EasyPaisa'),
        ('bank_transfer', 'Bank Transfer'),
    ])
    coupon_code = serializers.CharField(max_length=50, required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_status', 'notes']
