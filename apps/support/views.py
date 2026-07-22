from rest_framework import generics, permissions

from .models import FAQ, SupportTicket, TicketMessage
from .serializers import FAQSerializer, SupportTicketSerializer, TicketMessageSerializer


class FAQListView(generics.ListAPIView):
    queryset = FAQ.objects.filter(is_active=True)
    serializer_class = FAQSerializer
    permission_classes = [permissions.AllowAny]


class SupportTicketListCreateView(generics.ListCreateAPIView):
    serializer_class = SupportTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SupportTicket.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SupportTicketDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = SupportTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SupportTicket.objects.filter(user=self.request.user)


class TicketMessageCreateView(generics.CreateAPIView):
    serializer_class = TicketMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        ticket = get_object_or_404(SupportTicket, pk=self.kwargs.get("ticket_pk"))
        if ticket.user != self.request.user:
            raise PermissionDenied("You are not allowed to message this ticket.")
        serializer.save(ticket=ticket, user=self.request.user)
