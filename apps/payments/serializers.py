from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class PaymentInitiateSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(choices=Payment._meta.get_field('payment_method').choices)
