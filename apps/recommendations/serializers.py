from rest_framework import serializers
from .models import ProductRecommendation, UserPreference


class ProductRecommendationSerializer(serializers.ModelSerializer):
    recommended_product_name = serializers.CharField(source='recommended_product.name', read_only=True)
    recommended_product_image = serializers.SerializerMethodField()
    recommended_product_price = serializers.DecimalField(source='recommended_product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = ProductRecommendation
        fields = ['id', 'product', 'recommended_product', 'recommended_product_name', 'recommended_product_image', 'recommended_product_price', 'score', 'reason', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_recommended_product_image(self, obj):
        request = self.context.get('request')
        primary = obj.recommended_product.images.filter(is_primary=True).first()
        if primary and primary.image and request:
            return request.build_absolute_uri(primary.image.url)
        return None


class UserPreferenceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = UserPreference
        fields = ['id', 'user', 'category', 'category_name', 'score', 'updated_at']
        read_only_fields = ['id', 'updated_at']
