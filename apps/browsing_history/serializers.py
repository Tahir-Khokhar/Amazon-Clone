from rest_framework import serializers
from .models import BrowsingHistory


class BrowsingHistorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.SlugField(source='product.slug', read_only=True)
    product_image = serializers.SerializerMethodField()
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_discount_price = serializers.DecimalField(source='product.discount_price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = BrowsingHistory
        fields = ['id', 'user', 'product', 'product_name', 'product_slug', 'product_image', 'product_price', 'product_discount_price', 'viewed_at']
        read_only_fields = ['id', 'viewed_at']

    def get_product_image(self, obj):
        request = self.context.get('request')
        primary = obj.product.images.filter(is_primary=True).first()
        if primary and primary.image and request:
            return request.build_absolute_uri(primary.image.url)
        return None
