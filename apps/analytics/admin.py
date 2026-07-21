from django.contrib import admin
from .models import PageView, ProductView


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['path', 'user', 'ip_address', 'created_at']
    list_filter = ['created_at', 'method']
    search_fields = ['path', 'user__username', 'ip_address']
    readonly_fields = ['created_at']


@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'ip_address', 'created_at']
    list_filter = ['created_at']
    search_fields = ['product__name', 'user__username', 'ip_address']
    readonly_fields = ['created_at']
