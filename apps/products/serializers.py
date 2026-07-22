from rest_framework import serializers
from .models import Tag, ProductAttribute, ProductAttributeValue, ProductImage, ProductVariant, Inventory, Product


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = '__all__'


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class ProductVariantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'sku', 'name', 'price', 'discount_price', 'stock', 'color', 'size']


class ProductVariantSerializer(serializers.ModelSerializer):
    inventory = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'sku', 'name', 'price', 'discount_price', 'stock', 'color', 'size', 'weight', 'is_active', 'inventory']
        read_only_fields = ['id']


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductListSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    seller = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'discount_price', 'thumbnail', 'brand', 'category', 'seller', 'is_featured', 'is_active', 'views_count', 'sales_count', 'tags']


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantListSerializer(many=True, read_only=True)
    attribute_values = ProductAttributeValueSerializer(many=True, read_only=True)
    brand = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    seller = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'description', 'short_description', 'price', 'discount_price',
            'stock', 'sku', 'barcode', 'brand', 'category', 'seller', 'thumbnail',
            'weight', 'material', 'warranty', 'is_featured', 'is_active', 'tags'
        ]
