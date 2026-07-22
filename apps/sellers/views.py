from rest_framework import generics, permissions

from .models import SellerProfile
from .serializers import SellerDashboardSerializer, SellerProductSerializer, SellerOrderSerializer


class SellerDashboardView(generics.ListAPIView):
    serializer_class = SellerDashboardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SellerProfile.objects.filter(user=self.request.user)


class SellerProductsView(generics.ListAPIView):
    serializer_class = SellerProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        from products.models import Product
        return Product.objects.filter(seller=self.request.user)


class SellerOrdersView(generics.ListAPIView):
    serializer_class = SellerOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        from orders.models import Order
        return Order.objects.filter(items__product__seller=self.request.user).distinct()


class SellerCouponsView(generics.ListAPIView):
    serializer_class = SellerProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        from coupons.models import Coupon
        return Coupon.objects.filter(created_by=self.request.user)


class SellerAnalyticsView(generics.ListAPIView):
    serializer_class = SellerDashboardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SellerProfile.objects.filter(user=self.request.user)
