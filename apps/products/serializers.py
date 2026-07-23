from rest_framework import serializers

from .models import (
    Inventory,
    Product,
    ProductAttribute,
    ProductAttributeValue,
    ProductImage,
    ProductSpecification,
    ProductStatus,
    ProductVariant,
    Tag,
)


# ============================================================================
# Helper serializers (Tags, Attributes, etc.)
# ============================================================================

class TagSerializer(serializers.ModelSerializer):
    """Serializer for the Tag model."""

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id', 'slug']


class ProductAttributeSerializer(serializers.ModelSerializer):
    """Serializer for ProductAttribute (attribute definitions)."""

    class Meta:
        model = ProductAttribute
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id', 'slug']


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    """Serializer for attribute values linked to a product."""

    attribute_name = serializers.CharField(source='attribute.name', read_only=True)

    class Meta:
        model = ProductAttributeValue
        fields = ['id', 'attribute', 'attribute_name', 'value']
        read_only_fields = ['id']


class InventorySerializer(serializers.ModelSerializer):
    """Serializer for the Inventory model (optional)."""

    class Meta:
        model = Inventory
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


# ============================================================================
# ProductImage
# ============================================================================

class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for product images."""

    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image', 'image_url', 'alt_text', 'is_primary', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'product': {'write_only': True},
        }

    def get_image_url(self, obj):
        """Return full URL of the image if available."""
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def validate(self, data):
        """Ensure at most one primary image per product."""
        if data.get('is_primary') and data.get('product'):
            product = data['product']
            qs = ProductImage.objects.filter(product=product, is_primary=True)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {"is_primary": "This product already has a primary image."}
                )
        return data


# ============================================================================
# ProductVariant
# ============================================================================

class ProductVariantSerializer(serializers.ModelSerializer):
    """Full serializer for ProductVariant (read/write)."""

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = [
            'id', 'product', 'sku', 'name', 'additional_price', 'stock',
            'color', 'size', 'weight', 'is_active', 'total_price',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'product': {'write_only': True},
        }

    def get_total_price(self, obj):
        """Calculate total price = base product price + variant additional price."""
        if obj.product_id:
            base = obj.product.price
            return float(base) + float(obj.additional_price)
        return float(obj.additional_price)

    def validate_stock(self, value):
        """Prevent negative stock values."""
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value

    def validate_sku(self, value):
        """Check SKU uniqueness (case-insensitive)."""
        qs = ProductVariant.objects.filter(sku__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A variant with this SKU already exists.")
        return value


class ProductVariantListSerializer(serializers.ModelSerializer):
    """Lightweight variant serializer for list endpoints."""

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = ['id', 'sku', 'name', 'additional_price', 'stock', 'color', 'size', 'total_price']
        read_only_fields = fields

    def get_total_price(self, obj):
        if obj.product_id:
            base = obj.product.price
            return float(base) + float(obj.additional_price)
        return float(obj.additional_price)


# ============================================================================
# ProductSpecification
# ============================================================================

class ProductSpecificationSerializer(serializers.ModelSerializer):
    """Serializer for product key-value specifications."""

    class Meta:
        model = ProductSpecification
        fields = ['id', 'product', 'key', 'value']
        read_only_fields = ['id']
        extra_kwargs = {
            'product': {'write_only': True},
        }

    def validate(self, data):
        """Ensure key is not empty."""
        if not data.get('key', '').strip():
            raise serializers.ValidationError({"key": "Specification key cannot be empty."})
        if not data.get('value', '').strip():
            raise serializers.ValidationError({"value": "Specification value cannot be empty."})
        return data


# ============================================================================
# Product – Main Serializers
# ============================================================================

class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight read-only serializer for product list endpoints."""

    brand = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    thumbnail_url = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'discount_price',
            'thumbnail', 'thumbnail_url', 'primary_image',
            'brand', 'category', 'is_featured', 'is_active',
            'status', 'average_rating', 'total_reviews',
            'stock', 'views_count', 'sales_count',
            'created_at',
        ]
        read_only_fields = fields

    def get_thumbnail_url(self, obj):
        """Return full thumbnail URL if available."""
        request = self.context.get('request')
        if obj.thumbnail and request:
            return request.build_absolute_uri(obj.thumbnail.url)
        return None

    def get_primary_image(self, obj):
        """Return the URL of the primary image if available."""
        request = self.context.get('request')
        primary = obj.images.filter(is_primary=True).first()
        if primary and primary.image and request:
            return request.build_absolute_uri(primary.image.url)
        return None

    def to_representation(self, instance):
        """Optimize by annotating the primary image URL."""
        data = super().to_representation(instance)
        # Show effective price (discount price if available)
        if instance.discount_price:
            data['effective_price'] = float(instance.discount_price)
        else:
            data['effective_price'] = float(instance.price)
        return data


class ProductDetailSerializer(serializers.ModelSerializer):
    """Full read-only serializer for product detail view."""

    # Nested read-only relations
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantListSerializer(many=True, read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)
    attribute_values = ProductAttributeValueSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    # String representations of foreign keys
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    brand_slug = serializers.SlugField(source='brand.slug', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.SlugField(source='category.slug', read_only=True)
    seller_username = serializers.CharField(source='seller.username', read_only=True)

    thumbnail_url = serializers.SerializerMethodField()
    effective_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = [
            'id', 'slug', 'views_count', 'sales_count',
            'average_rating', 'total_reviews',
            'created_at', 'updated_at',
        ]

    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        if obj.thumbnail and request:
            return request.build_absolute_uri(obj.thumbnail.url)
        return None

    def get_effective_price(self, obj):
        if obj.discount_price:
            return float(obj.discount_price)
        return float(obj.price)

    @staticmethod
    def setup_eager_loading(queryset):
        """Optimise queryset with select_related and prefetch_related."""
        return queryset.select_related(
            'brand', 'category', 'seller'
        ).prefetch_related(
            'images', 'variants', 'specifications',
            'attribute_values__attribute', 'tags'
        )


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Write serializer for creating / updating products with nested handling."""

    # Allow reading nested relations in responses
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), required=False
    )

    class Meta:
        model = Product
        fields = [
            # Identity
            'name', 'slug', 'short_description', 'full_description', 'description',
            # Relations
            'brand', 'category', 'seller', 'tags',
            # SKU & Pricing
            'sku', 'barcode', 'price', 'discount_price',
            # Stock
            'stock',
            # Media
            'thumbnail',
            # Physical
            'weight', 'material', 'warranty',
            # Status
            'status', 'is_featured', 'is_active',
            # Nested (read-only in this serializer)
            'images', 'variants', 'specifications',
        ]
        read_only_fields = ['slug', 'seller']

    # ---- Field-level validators ----

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value

    def validate_sku(self, value):
        """Check SKU uniqueness (case-insensitive)."""
        qs = Product.objects.filter(sku__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A product with this SKU already exists.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    # ---- Object-level validators ----

    def validate(self, data):
        """Cross-field validation."""
        errors = {}

        # Discount price must not exceed actual price
        discount_price = data.get('discount_price', getattr(self.instance, 'discount_price', None))
        price = data.get('price', getattr(self.instance, 'price', None))

        if discount_price is not None and price is not None:
            if discount_price > price:
                errors['discount_price'] = (
                    "Discount price cannot be greater than the actual price."
                )

        # Weighted warning for published products with 0 stock
        stock = data.get('stock', getattr(self.instance, 'stock', 0))
        if stock == 0:
            status = data.get('status', getattr(self.instance, 'status', None))
            if status == ProductStatus.PUBLISHED:
                errors['stock'] = (
                    "A published product cannot have zero stock. "
                    "Set status to 'draft' or 'out_of_stock'."
                )

        if errors:
            raise serializers.ValidationError(errors)

        return data

    # ---- Create / Update overrides ----

    def create(self, validated_data):
        """Create product and auto-assign seller from request user."""
        tags = validated_data.pop('tags', [])
        product = Product.objects.create(**validated_data)
        if tags:
            product.tags.set(tags)
        return product

    def update(self, instance, validated_data):
        """Update product fields and tags."""
        tags = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance
