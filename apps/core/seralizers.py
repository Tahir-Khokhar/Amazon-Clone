from rest_framework import serializers
from .models import SiteConfiguration


class SiteConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfiguration
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class ShippingRulesSerializer(serializers.Serializer):
    free_shipping_threshold = serializers.DecimalField(max_digits=10, decimal_places=2)
    standard_shipping_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    express_shipping_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency_symbol = serializers.CharField(max_length=5)
    is_free_shipping = serializers.BooleanField()


class ReturnPolicySerializer(serializers.Serializer):
    return_window_days = serializers.IntegerField()
    auto_approve_returns = serializers.BooleanField()
    refund_processing_days = serializers.IntegerField()
    can_return = serializers.BooleanField()
    days_remaining = serializers.IntegerField(allow_null=True)


class PaymentMethodsSerializer(serializers.Serializer):
    methods = serializers.ListField(child=serializers.DictField())
    secure_payment = serializers.BooleanField()


class SupportInfoSerializer(serializers.Serializer):
    available_247 = serializers.BooleanField()
    response_hours = serializers.CharField()
    sla_hours = serializers.IntegerField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    is_open = serializers.BooleanField()
