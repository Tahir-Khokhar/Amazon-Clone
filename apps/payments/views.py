from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer, PaymentInitiateSerializer


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(order__user=self.request.user)


class PaymentDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(order__user=self.request.user)


class PaymentInitiateView(generics.GenericAPIView):
    serializer_class = PaymentInitiateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()
        return Response(
            PaymentSerializer(payment).data,
            status=status.HTTP_201_CREATED,
        )


class PaymentWebhookView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        transaction_id = data.get("transaction_id")
        payment_status = data.get("status")
        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
            payment.payment_status = payment_status
            payment.payment_data = data
            payment.save()
            if payment_status == "completed":
                payment.order.payment_status = "completed"
                payment.order.save()
            return Response({"message": "Webhook processed."}, status=status.HTTP_200_OK)
        except Payment.DoesNotExist:
            return Response(
                {"detail": "Payment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
