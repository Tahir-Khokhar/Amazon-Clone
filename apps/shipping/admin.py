from django.contrib import admin
from .models import SellerProfile


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'store_name', 'is_verified', 'is_active', 'commission_rate', 'total_sales', 'total_revenue', 'created_at']
    list_filter = ['is_verified', 'is_active']
    search_fields = ['user__username', 'store_name', 'phone_number']
    readonly_fields = ['total_sales', 'total_revenue', 'created_at', 'updated_at']
