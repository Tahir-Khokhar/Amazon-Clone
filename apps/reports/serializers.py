from rest_framework import serializers
from .models import SalesReport, TopProduct, TopCategory


class SalesReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesReport
        fields = '__all__'
        read_only_fields = ['id']


class TopProductSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = TopProduct
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class TopCategorySerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = TopCategory
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
