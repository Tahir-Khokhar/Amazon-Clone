from rest_framework import serializers
from .models import CustomerProfile


class CustomerDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = '__all__'
        read_only_fields = ['id']


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = '__all__'
        read_only_fields = ['id']
