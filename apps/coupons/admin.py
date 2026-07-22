from django.contrib import admin
from .models import Coupon, CouponUsage


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'coupon_type', 'discount_value', 'is_active', 'valid_from', 'valid_until', 'used_count', 'usage_limit']
    list_filter = ['coupon_type', 'is_active', 'valid_from', 'valid_until']
    search_fields = ['code']
    readonly_fields = ['used_count', 'created_at', 'updated_at']


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ['coupon', 'user', 'order', 'used_at']
    list_filter = ['used_at']
    search_fields = ['coupon__code', 'user__username', 'order__order_number']
    readonly_fields = ['used_at']
