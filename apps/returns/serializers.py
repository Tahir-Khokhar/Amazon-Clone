from django.utils import timezone
from rest_framework import serializers
from .models import ReturnRequest


class ReturnRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnRequest
        fields = '__all__'
        read_only_fields = ['id', 'user', 'status', 'admin_note', 'refund_amount', 'created_at', 'updated_at']


class ReturnRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnRequest
        fields = ['order', 'order_item', 'return_type', 'reason', 'description', 'images']

    def validate_order_item(self, value):
        if value.order.user != self.context['request'].user:
            raise serializers.ValidationError('This order item does not belong to you.')
        if value.order.order_status != 'delivered':
            raise serializers.ValidationError('Only delivered orders can be returned.')
        return value

    def validate(self, attrs):
        
        from apps.core.models import SiteConfiguration
        config = SiteConfiguration.get_active()
        if config:
            order = attrs.get('order')
            if order and order.ordered_at:
                days_since = (timezone.now().date() - order.ordered_at.date()).days
                if days_since > config.return_window_days:
                    raise serializers.ValidationError(
                        f'Return window of {config.return_window_days} days has expired.'
                    )
        return attrs


class ReturnRequestAdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnRequest
        fields = ['status', 'admin_note', 'refund_amount']
