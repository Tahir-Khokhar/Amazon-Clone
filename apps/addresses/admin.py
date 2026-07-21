from django.contrib import admin
from .models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'city', 'country', 'address_type', 'is_default', 'created_at']
    list_filter = ['country', 'address_type', 'is_default', 'created_at']
    search_fields = ['user__username', 'full_name', 'city', 'postal_code']
