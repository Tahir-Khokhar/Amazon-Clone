from django.urls import path
from .views import (
    ChatRoomListView,
    ChatRoomDetailView,
    ChatRoomCreateView,
    ChatMessageListView,
    ChatMessageCreateView,
    MarkMessagesReadView,
)

app_name = 'chat'

urlpatterns = [
    path('rooms/', ChatRoomListView.as_view(), name='room-list'),
    path('rooms/create/', ChatRoomCreateView.as_view(), name='room-create'),
    path('rooms/<int:pk>/', ChatRoomDetailView.as_view(), name='room-detail'),
    path('rooms/<int:room_pk>/messages/', ChatMessageListView.as_view(), name='message-list'),
    path('rooms/<int:room_pk>/messages/create/', ChatMessageCreateView.as_view(), name='message-create'),
    path('rooms/<int:room_pk>/messages/read/', MarkMessagesReadView.as_view(), name='messages-read'),
]
