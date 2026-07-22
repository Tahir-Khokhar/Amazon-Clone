from rest_framework import generics, permissions

from .models import DashboardStat
from .serializers import AdminDashboardSerializer


class AdminDashboardView(generics.ListAPIView):
    serializer_class = AdminDashboardSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return DashboardStat.objects.all()[:30]


class SellerDashboardView(generics.ListAPIView):
    serializer_class = AdminDashboardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "seller":
            return DashboardStat.objects.all()[:30]
        return DashboardStat.objects.none()
