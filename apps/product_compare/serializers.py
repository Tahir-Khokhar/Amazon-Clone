from rest_framework import serializers
from .models import CompareList, CompareItem


class CompareItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_discount_price = serializers.DecimalField(source='product.discount_price', max_digits=10, decimal_places=2, read_only=True)
    product_image = serializers.SerializerMethodField()
    product_rating = serializers.DecimalField(source='product.average_rating', max_digits=3, decimal_places=2, read_only=True)

    class Meta:
        model = CompareItem
        fields = ['id', 'compare_list', 'product', 'product_name', 'product_price', 'product_discount_price', 'product_image', 'product_rating', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_product_image(self, obj):
        request = self.context.get('request')
        primary = obj.product.images.filter(is_primary=True).first()
        if primary and primary.image and request:
            return request.build_absolute_uri(primary.image.url)
        return None


class CompareListSerializer(serializers.ModelSerializer):
    items = CompareItemSerializer(many=True, read_only=True)
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = CompareList
        fields = ['id', 'user', 'items', 'item_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_item_count(self, obj):
        return obj.items.count()
