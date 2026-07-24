from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatRoomCreateSerializer, ChatMessageSerializer


class ChatRoomListView(generics.ListAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'seller':
            return ChatRoom.objects.filter(seller=user, is_active=True)
        return ChatRoom.objects.filter(customer=user, is_active=True)


class ChatRoomDetailView(generics.RetrieveAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'seller':
            return ChatRoom.objects.filter(seller=user, is_active=True)
        return ChatRoom.objects.filter(customer=user, is_active=True)


class ChatRoomCreateView(generics.CreateAPIView):
    serializer_class = ChatRoomCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class ChatMessageListView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room = get_object_or_404(ChatRoom, pk=self.kwargs.get('room_pk'))
        if self.request.user not in [room.customer, room.seller]:
            return ChatMessage.objects.none()
        return room.messages.all()


class ChatMessageCreateView(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        room = get_object_or_404(ChatRoom, pk=self.kwargs.get('room_pk'))
        if self.request.user not in [room.customer, room.seller]:
            raise serializers.ValidationError('You are not a member of this chat room.')
        message = serializer.save(room=room, sender=self.request.user)
        room.updated_at = message.created_at
        room.save()


class MarkMessagesReadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        room = get_object_or_404(ChatRoom, pk=kwargs.get('room_pk'))
        if request.user not in [room.customer, room.seller]:
            return Response({"error": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        room.messages.exclude(sender=request.user).update(is_read=True)
        return Response({"message": "Messages marked as read."}, status=status.HTTP_200_OK)
