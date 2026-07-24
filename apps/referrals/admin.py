from django.contrib import admin
from .models import ReferralCode, Referral


@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'is_active', 'created_at']
    search_fields = ['user__username', 'code']


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['referrer', 'referred_user', 'order', 'reward_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
