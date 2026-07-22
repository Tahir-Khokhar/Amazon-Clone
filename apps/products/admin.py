from django.contrib import admin
from .models import Tag, ProductAttribute, ProductAttributeValue, ProductImage, ProductVariant, Inventory, Product


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    raw_id_fields = ['product']


class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ['attribute', 'value', 'product']
    list_filter = ['attribute']
    search_fields = ['attribute__name', 'value', 'product__name']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__name']
    raw_id_fields = ['product']


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'sku', 'price', 'stock', 'color', 'size', 'is_active']
    list_filter = ['is_active', 'color', 'size']
    search_fields = ['product__name', 'name', 'sku']
    raw_id_fields = ['product']


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['product_variant', 'stock_available', 'stock_reserved', 'stock_sold', 'low_stock_threshold', 'last_restocked']
    list_filter = ['last_restocked']
    search_fields = ['product_variant__name', 'product_variant__sku']
    raw_id_fields = ['product_variant']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'discount_price', 'stock', 'brand', 'category', 'seller', 'is_featured', 'is_active', 'created_at']
    list_filter = ['is_featured', 'is_active', 'brand', 'category', 'created_at']
    search_fields = ['name', 'slug', 'sku', 'barcode', 'seller__username']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['views_count', 'sales_count', 'created_at', 'updated_at']
    inlines = [ProductImageInline, ProductVariantInline, ProductAttributeValueInline]
    filter_horizontal = ['tags']
