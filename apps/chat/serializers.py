from rest_framework import serializers
from .models import ChatRoom, ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()

    class Meta:
        model = ChatMessage
        fields = ['id', 'room', 'sender', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']


class ChatRoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    other_user = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'customer', 'seller', 'is_active', 'last_message', 'unread_count', 'other_user', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_last_message(self, obj):
        last = obj.messages.last()
        if last:
            return last.message
        return None

    def get_unread_count(self, obj):
        user = self.context['request'].user
        return obj.messages.filter(is_read=False).exclude(sender=user).count()

    def get_other_user(self, obj):
        user = self.context['request'].user
        other = obj.seller if user == obj.customer else obj.customer
        return {
            'id': other.id,
            'username': other.username,
            'first_name': other.first_name,
            'last_name': other.last_name,
        }


class ChatRoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['seller']

    def validate_seller(self, value):
        if value.role != 'seller':
            raise serializers.ValidationError('You can only chat with sellers.')
        return value
