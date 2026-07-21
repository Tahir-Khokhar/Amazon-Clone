from django.contrib import admin
from .models import User, Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_verified', 'is_staff', 'date_joined']
    list_filter = ['role', 'is_verified', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'phone_number']
    readonly_fields = ['date_joined', 'last_login']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'gender', 'date_of_birth']
    search_fields = ['user__username', 'user__email', 'phone_number']
