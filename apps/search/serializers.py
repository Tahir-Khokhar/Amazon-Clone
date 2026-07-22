from rest_framework import serializers
from .models import Review, ReviewLike


class ReviewSerializer(serializers.ModelSerializer):
    images = serializers.JSONField()
    product = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'title', 'comment', 'images', 'is_verified_purchase', 'helpful_count', 'is_approved', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=__import__('apps.products.models', fromlist=['Product']).Product.objects.filter(is_active=True))
    images = serializers.JSONField(required=False, default=list)

    class Meta:
        model = Review
        fields = ['product', 'rating', 'title', 'comment', 'images']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value

    def validate(self, data):
        user = self.context['request'].user
        product = data['product']
        if Review.objects.filter(product=product, user=user).exists():
            raise serializers.ValidationError('You have already reviewed this product.')

        from orders.models import OrderItem
        has_purchased = OrderItem.objects.filter(order__user=user, product=product, order__order_status='delivered').exists()
        data['is_verified_purchase'] = has_purchased
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ReviewLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewLike
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class ReviewReportSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=200)
    details = serializers.CharField(required=False, allow_blank=True)
