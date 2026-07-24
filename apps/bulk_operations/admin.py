from django.contrib import admin
from .models import ImportJob


@admin.register(ImportJob)
class ImportJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'file_type', 'status', 'created_at', 'completed_at']
    list_filter = ['status', 'file_type', 'created_at']
    search_fields = ['user__username', 'file_name']
