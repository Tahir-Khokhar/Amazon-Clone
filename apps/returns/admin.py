from django.contrib import admin
from .models import ReturnRequest


@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'order_item', 'user', 'return_type', 'reason', 'status', 'created_at']
    list_filter = ['status', 'return_type', 'reason', 'created_at']
    search_fields = ['order__order_number', 'user__username', 'description']
    readonly_fields = ['created_at', 'updated_at']
