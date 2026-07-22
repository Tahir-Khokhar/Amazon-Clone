from django.contrib import admin
from .models import CustomerProfile


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_orders', 'total_spent', 'loyalty_points', 'is_premium']
    list_filter = ['is_premium']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['total_orders', 'total_spent', 'wishlist_count', 'loyalty_points']
