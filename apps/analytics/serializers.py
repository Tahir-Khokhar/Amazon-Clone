from rest_framework import serializers
from .models import PageView, ProductView


class PageViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageView
        fields = '__all__'
        read_only_fields = ['created_at']


class ProductViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductView
        fields = '__all__'
        read_only_fields = ['created_at']
