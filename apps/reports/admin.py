from django.contrib import admin
from .models import SalesReport, TopProduct, TopCategory


@admin.register(SalesReport)
class SalesReportAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_orders', 'total_revenue', 'total_products_sold', 'total_customers']
    list_filter = ['date']
    search_fields = ['date']
    readonly_fields = ['date', 'total_orders', 'total_revenue', 'total_products_sold', 'total_customers']


@admin.register(TopProduct)
class TopProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'total_sales', 'total_revenue', 'total_orders', 'period_start', 'period_end']
    list_filter = ['period_start', 'period_end']
    search_fields = ['product__name']
    raw_id_fields = ['product']


@admin.register(TopCategory)
class TopCategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'total_sales', 'total_revenue', 'period_start', 'period_end']
    list_filter = ['period_start', 'period_end']
    search_fields = ['category__name']
    raw_id_fields = ['category']
