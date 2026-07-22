from django.contrib import admin
from .models import DashboardStat


@admin.register(DashboardStat)
class DashboardStatAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_orders', 'total_revenue', 'total_users', 'total_products']
    list_filter = ['date']
    search_fields = ['date']
    readonly_fields = ['date', 'total_orders', 'total_revenue', 'total_users', 'total_products', 'new_orders', 'new_users']
