from rest_framework import serializers
from .models import Coupon, CouponUsage


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'
        read_only_fields = ['id', 'used_count', 'created_at', 'updated_at']


class CouponValidateSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50)
    order_amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)

    def validate(self, data):
        from django.utils import timezone
        try:
            coupon = Coupon.objects.get(code=data['code'])
        except Coupon.DoesNotExist:
            raise serializers.ValidationError({'code': 'Invalid coupon code.'})

        if not coupon.is_active:
            raise serializers.ValidationError({'code': 'Coupon is not active.'})

        if coupon.valid_from > timezone.now():
            raise serializers.ValidationError({'code': 'Coupon is not yet valid.'})

        if coupon.valid_until < timezone.now():
            raise serializers.ValidationError({'code': 'Coupon has expired.'})

        if coupon.usage_limit > 0 and coupon.used_count >= coupon.usage_limit:
            raise serializers.ValidationError({'code': 'Coupon usage limit reached.'})

        if data['order_amount'] < coupon.minimum_purchase:
            raise serializers.ValidationError({
                'order_amount': f"Minimum purchase of {coupon.minimum_purchase} required to use this coupon."
            })

        data['coupon'] = coupon
        return data
