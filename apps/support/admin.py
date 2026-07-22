from django.contrib import admin
from .models import FAQ, SupportTicket, TicketMessage


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'is_active', 'order', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['question', 'answer']
    readonly_fields = ['created_at', 'updated_at']


class TicketMessageInline(admin.TabularInline):
    model = TicketMessage
    extra = 0
    raw_id_fields = ['user']


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'ticket_status', 'priority', 'created_at', 'resolved_at']
    list_filter = ['ticket_status', 'priority', 'created_at']
    search_fields = ['user__username', 'subject', 'description']
    readonly_fields = ['created_at', 'updated_at', 'resolved_at']
    inlines = [TicketMessageInline]


@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['ticket__subject', 'user__username', 'message']
    raw_id_fields = ['ticket', 'user']
    readonly_fields = ['created_at']
