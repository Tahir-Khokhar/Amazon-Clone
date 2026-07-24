from django.contrib import admin
from .models import ChatRoom, ChatMessage

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'seller', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['customer__username', 'seller__username']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['room', 'sender', 'message', 'created_at']
    list_filter = ['created_at']
    search_fields = ['message', 'sender__username']
