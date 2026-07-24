from rest_framework import serializers
from .models import ReferralCode, Referral


class ReferralCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralCode
        fields = ['id', 'user', 'code', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class ReferralSerializer(serializers.ModelSerializer):
    referrer_username = serializers.CharField(source='referrer.username', read_only=True)
    referred_username = serializers.CharField(source='referred_user.username', read_only=True)

    class Meta:
        model = Referral
        fields = ['id', 'referrer', 'referrer_username', 'referred_user', 'referred_username', 'order', 'reward_amount', 'status', 'created_at', 'completed_at']
        read_only_fields = ['id', 'created_at', 'completed_at']
