from rest_framework import serializers
from .models import DashboardStat


class AdminDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardStat
        fields = '__all__'
        read_only_fields = ['id']


class SellerDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardStat
        fields = '__all__'
        read_only_fields = ['id']
