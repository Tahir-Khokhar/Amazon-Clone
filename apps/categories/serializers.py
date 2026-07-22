from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'image', 'icon', 'is_active', 'featured', 'children']

    def get_children(self, obj):
        if obj.parent is None:
            return CategorySerializer(obj.children.filter(is_active=True), many=True).data
        return []


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'image']


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent', 'image', 'icon', 'is_active', 'featured']
