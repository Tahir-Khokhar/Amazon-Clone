from django.contrib import admin
from .models import CompareList, CompareItem

@admin.register(CompareList)
class CompareListAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__username']

@admin.register(CompareItem)
class CompareItemAdmin(admin.ModelAdmin):
    list_display = ['compare_list', 'product', 'created_at']
    list_filter = ['created_at']
