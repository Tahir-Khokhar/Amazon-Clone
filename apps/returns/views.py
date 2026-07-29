from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.core.models import SiteConfiguration
from .models import ReturnRequest
from .serializers import ReturnRequestSerializer, ReturnRequestCreateSerializer, ReturnRequestAdminUpdateSerializer


class ReturnRequestListView(generics.ListAPIView):
    serializer_class = ReturnRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ReturnRequest.objects.none()
        user = self.request.user
        if user.role == 'admin':
            return ReturnRequest.objects.all()
        return ReturnRequest.objects.filter(user=user)


class ReturnRequestDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ReturnRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ReturnRequest.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return ReturnRequest.objects.all()
        return ReturnRequest.objects.filter(user=user)


class ReturnRequestCreateView(generics.CreateAPIView):
    serializer_class = ReturnRequestCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        config = SiteConfiguration.get_active()
        order_item = serializer.validated_data.get('order_item')
        order = order_item.order if order_item else None

        if order and config:
            return_window = config.return_window_days
            if order.ordered_at:
                days_since = (timezone.now().date() - order.ordered_at.date()).days
                if days_since > return_window:
                    raise serializers.ValidationError(
                        f'Return window of {return_window} days has expired.'
                    )

        return_request = serializer.save(user=self.request.user)

        if config and config.auto_approve_returns:
            return_request.status = 'approved'
            return_request.admin_note = 'Auto-approved by system.'
            return_request.save()


class ReturnRequestAdminUpdateView(generics.UpdateAPIView):
    serializer_class = ReturnRequestAdminUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = ReturnRequest.objects.all()
