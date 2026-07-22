from django.db.models import F
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Coupon, CouponUsage
from .serializers import CouponSerializer, CouponValidateSerializer


class CouponListView(generics.ListAPIView):
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        now = timezone.now()
        return Coupon.objects.filter(
            is_active=True,
            valid_from__lte=now,
            valid_until__gte=now,
        ).exclude(usage_limit__gt=0, used_count__gte=F("usage_limit"))


class CouponDetailView(generics.RetrieveAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "code"


class CouponValidateView(generics.GenericAPIView):
    serializer_class = CouponValidateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        coupon = serializer.validated_data["coupon"]
        return Response(
            {
                "code": coupon.code,
                "coupon_type": coupon.coupon_type,
                "discount_value": coupon.discount_value,
                "message": "Coupon is valid.",
            },
            status=status.HTTP_200_OK,
        )


class CouponCreateView(generics.CreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAdminUser]
