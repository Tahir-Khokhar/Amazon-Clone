from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

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
# Inlines
# ============================================================================

class ProductImageInline(admin.TabularInline):
    """Inline admin for product images with thumbnail preview."""

    model = ProductImage
    extra = 1
    readonly_fields = ['image_preview', 'created_at']
    fields = ['image_preview', 'image', 'alt_text', 'is_primary', 'created_at']

    def image_preview(self, obj):
        """Show a small thumbnail of the image."""
        if obj.image and hasattr(obj.image, 'url'):
            return format_html(
                '<img src="{}" style="width: 80px; height: 80px; object-fit: cover; '
                'border-radius: 4px;" />',
                obj.image.url,
            )
        return "—"

    image_preview.short_description = _("Preview")


class ProductVariantInline(admin.TabularInline):
    """Inline admin for product variants."""

    model = ProductVariant
    extra = 0
    raw_id_fields = ['product']
    fields = ['sku', 'name', 'additional_price', 'stock', 'color', 'size', 'weight', 'is_active']


class ProductSpecificationInline(admin.TabularInline):
    """Inline admin for product specifications."""

    model = ProductSpecification
    extra = 1
    fields = ['key', 'value']


class ProductAttributeValueInline(admin.TabularInline):
    """Inline admin for product attribute values."""

    model = ProductAttributeValue
    extra = 1
    fields = ['attribute', 'value']


# ============================================================================
# Model Admins
# ============================================================================

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin for product tags."""

    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    """Admin for product attribute definitions."""

    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    """Admin for product attribute values."""

    list_display = ['attribute', 'value', 'product']
    list_filter = ['attribute']
    search_fields = ['attribute__name', 'value', 'product__name']
    raw_id_fields = ['product']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Admin for product images."""

    list_display = ['thumbnail_preview', 'product', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__name']
    raw_id_fields = ['product']
    readonly_fields = ['image_preview', 'created_at']

    def thumbnail_preview(self, obj):
        """Display a small thumbnail in the list view."""
        if obj.image and hasattr(obj.image, 'url'):
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; object-fit: cover; '
                'border-radius: 4px;" />',
                obj.image.url,
            )
        return "—"

    thumbnail_preview.short_description = _("Image")

    def image_preview(self, obj):
        """Display a larger preview in the detail view."""
        if obj.image and hasattr(obj.image, 'url'):
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; '
                'object-fit: contain; border-radius: 4px;" />',
                obj.image.url,
            )
        return "—"

    image_preview.short_description = _("Image Preview")


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    """Admin for product variants."""

    list_display = [
        'product', 'name', 'sku', 'additional_price', 'stock',
        'color', 'size', 'is_active',
    ]
    list_filter = ['is_active', 'color', 'size']
    search_fields = ['product__name', 'name', 'sku']
    raw_id_fields = ['product']


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    """Admin for product specifications."""

    list_display = ['product', 'key', 'value']
    list_filter = ['key']
    search_fields = ['product__name', 'key', 'value']
    raw_id_fields = ['product']


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    """Admin for inventory tracking."""

    list_display = [
        'product_variant', 'stock_available', 'stock_reserved',
        'stock_sold', 'low_stock_threshold', 'last_restocked',
    ]
    list_filter = ['last_restocked']
    search_fields = ['product_variant__name', 'product_variant__sku']
    raw_id_fields = ['product_variant']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Comprehensive admin for the Product model."""

    # ---- List Display ----
    list_display = [
        'thumbnail_preview', 'name', 'sku', 'price', 'discount_price',
        'stock', 'status_badge', 'is_featured', 'is_active',
        'average_rating', 'brand', 'category', 'created_at',
    ]
    list_display_links = ['thumbnail_preview', 'name']

    # ---- List Filters ----
    list_filter = [
        'status', 'is_featured', 'is_active', 'brand', 'category',
        'created_at', 'updated_at',
    ]

    # ---- Search ----
    search_fields = [
        'name', 'slug', 'sku', 'barcode',
        'short_description', 'full_description',
        'seller__username', 'seller__email',
    ]

    # ---- Slug auto-populate ----
    prepopulated_fields = {'slug': ('name',)}

    # ---- Read-only fields ----
    readonly_fields = [
        'thumbnail_preview_large', 'average_rating', 'total_reviews',
        'views_count', 'sales_count', 'created_at', 'updated_at',
    ]

    # ---- Fieldsets (organise the form) ----
    fieldsets = (
        (None, {
            'fields': ('thumbnail_preview_large', 'thumbnail', 'name', 'slug'),
        }),
        (_("Description"), {
            'fields': ('short_description', 'full_description', 'description'),
        }),
        (_("Pricing & Stock"), {
            'fields': ('price', 'discount_price', 'stock', 'sku', 'barcode'),
        }),
        (_("Relations"), {
            'fields': ('brand', 'category', 'seller', 'tags'),
        }),
        (_("Physical Attributes"), {
            'fields': ('weight', 'material', 'warranty'),
        }),
        (_("Status & Flags"), {
            'fields': ('status', 'is_featured', 'is_active'),
        }),
        (_("Ratings & Tracking"), {
            'fields': ('average_rating', 'total_reviews', 'views_count', 'sales_count'),
        }),
        (_("Timestamps"), {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    # ---- Inlines ----
    inlines = [
        ProductImageInline,
        ProductVariantInline,
        ProductSpecificationInline,
        ProductAttributeValueInline,
    ]

    # ---- M2M widget ----
    filter_horizontal = ['tags']

    # ---- Optimize queries ----
    list_select_related = ['brand', 'category', 'seller']

    # ---- Ordering ----
    ordering = ['-created_at']

    # ---- Actions ----
    actions = ['make_published', 'make_draft', 'make_featured', 'remove_featured']

    # ------------------------------------------------------------------
    # Custom methods
    # ------------------------------------------------------------------

    def thumbnail_preview(self, obj):
        """Small thumbnail for list view."""
        if obj.thumbnail and hasattr(obj.thumbnail, 'url'):
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; object-fit: cover; '
                'border-radius: 4px;" />',
                obj.thumbnail.url,
            )
        return "—"

    thumbnail_preview.short_description = _("Thumbnail")

    def thumbnail_preview_large(self, obj):
        """Larger preview for detail view."""
        if obj.thumbnail and hasattr(obj.thumbnail, 'url'):
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; '
                'object-fit: contain; border-radius: 4px;" />',
                obj.thumbnail.url,
            )
        return _("No thumbnail uploaded.")

    thumbnail_preview_large.short_description = _("Thumbnail Preview")

    def status_badge(self, obj):
        """Colour-coded status badge."""
        colors = {
            ProductStatus.DRAFT: 'gray',
            ProductStatus.PUBLISHED: 'green',
            ProductStatus.OUT_OF_STOCK: 'red',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: white; background-color: {}; padding: 2px 8px; '
            'border-radius: 10px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = _("Status")
    status_badge.admin_order_field = 'status'

    # ------------------------------------------------------------------
    # Admin Actions
    # ------------------------------------------------------------------

    @admin.action(description=_("Mark selected products as Published"))
    def make_published(self, request, queryset):
        updated = queryset.update(status=ProductStatus.PUBLISHED)
        self.message_user(request, f"{updated} product(s) marked as Published.")

    @admin.action(description=_("Mark selected products as Draft"))
    def make_draft(self, request, queryset):
        updated = queryset.update(status=ProductStatus.DRAFT)
        self.message_user(request, f"{updated} product(s) marked as Draft.")

    @admin.action(description=_("Mark selected products as Featured"))
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f"{updated} product(s) marked as Featured.")

    @admin.action(description=_("Remove Featured from selected products"))
    def remove_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f"Featured removed from {updated} product(s).")
