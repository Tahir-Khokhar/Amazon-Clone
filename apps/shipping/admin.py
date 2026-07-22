from django.contrib import admin
from .models import ShippingMethod, ShippingAddress, Shipment


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_cost', 'estimated_delivery_days', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'city', 'country', 'is_default', 'created_at']
    list_filter = ['country', 'is_default', 'created_at']
    search_fields = ['user__username', 'full_name', 'city', 'postal_code']
    raw_id_fields = ['user']


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['order', 'shipping_method', 'courier_name', 'tracking_number', 'status', 'estimated_delivery', 'shipping_cost']
    list_filter = ['status', 'created_at']
    search_fields = ['order__order_number', 'tracking_number', 'courier_name']
    raw_id_fields = ['order', 'shipping_method']
    readonly_fields = ['created_at', 'updated_at']
