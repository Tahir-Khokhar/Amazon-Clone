from rest_framework import generics, permissions

from .models import CustomerProfile
from .serializers import CustomerDashboardSerializer, CustomerProfileSerializer


class CustomerDashboardView(generics.RetrieveAPIView):
    serializer_class = CustomerDashboardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.customer_profile


class CustomerOrdersView(generics.ListAPIView):
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        from orders.models import Order
        return Order.objects.filter(user=self.request.user)


class CustomerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.customer_profile
