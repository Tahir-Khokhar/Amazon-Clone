from rest_framework import generics, permissions

from .models import SalesReport, TopProduct, TopCategory
from .serializers import SalesReportSerializer, TopProductSerializer, TopCategorySerializer


class SalesReportView(generics.ListAPIView):
    queryset = SalesReport.objects.all()
    serializer_class = SalesReportSerializer
    permission_classes = [permissions.IsAdminUser]
    ordering = ["-date"]


class TopProductsView(generics.ListAPIView):
    queryset = TopProduct.objects.all()
    serializer_class = TopProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        user = self.request.user
        if user.is_staff or user.role in ["admin", "seller"]:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


class TopCategoriesView(generics.ListAPIView):
    queryset = TopCategory.objects.all()
    serializer_class = TopCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        user = self.request.user
        if user.is_staff or user.role in ["admin", "seller"]:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]
