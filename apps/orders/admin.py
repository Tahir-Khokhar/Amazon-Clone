from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ['product', 'variant']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'order_status', 'grand_total', 'payment_status', 'ordered_at']
    list_filter = ['order_status', 'payment_status', 'ordered_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    readonly_fields = ['ordered_at', 'updated_at']
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'product_sku', 'quantity', 'unit_price', 'total_price']
    list_filter = ['order__ordered_at']
    search_fields = ['order__order_number', 'product_name', 'product_sku']
    raw_id_fields = ['order', 'product', 'variant']
