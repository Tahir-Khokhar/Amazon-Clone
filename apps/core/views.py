from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import View
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import SiteConfiguration
from .serializers import (
    SiteConfigurationSerializer,
    ShippingRulesSerializer,
    ReturnPolicySerializer,
    PaymentMethodsSerializer,
    SupportInfoSerializer,
)


class HealthCheckView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({"status": "ok", "message": "API is healthy"})


class APIRootView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({
            "message": "Welcome to Amazon Clone API",
            "endpoints": {
                "auth": "/api/auth/",
                "categories": "/api/categories/",
                "brands": "/api/brands/",
                "products": "/api/products/",
                "cart": "/api/cart/",
                "wishlist": "/api/wishlist/",
                "orders": "/api/orders/",
                "payments": "/api/payments/",
                "shipping": "/api/shipping/",
                "coupons": "/api/coupons/",
                "reviews": "/api/reviews/",
                "notifications": "/api/notifications/",
                "addresses": "/api/addresses/",
                "search": "/api/search/",
                "dashboard": "/api/dashboard/",
                "reports": "/api/reports/",
                "analytics": "/api/analytics/",
                "support": "/api/support/",
                "customers": "/api/customers/",
                "sellers": "/api/sellers/",
                "core": "/api/core/",
            },
        })


class SiteConfigurationView(generics.RetrieveAPIView):
    serializer_class = SiteConfigurationSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return SiteConfiguration.get_active()


class ShippingRulesView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ShippingRulesSerializer

    def get(self, request, *args, **kwargs):
        config = SiteConfiguration.get_active()
        if not config:
            return Response({'detail': 'Site configuration not found.'}, status=status.HTTP_404_NOT_FOUND)

        subtotal = request.GET.get('subtotal', '0')
        try:
            subtotal = float(subtotal)
        except (TypeError, ValueError):
            subtotal = 0.0

        is_free = subtotal >= float(config.free_shipping_threshold)
        data = {
            'free_shipping_threshold': config.free_shipping_threshold,
            'standard_shipping_cost': config.standard_shipping_cost,
            'express_shipping_cost': config.express_shipping_cost,
            'currency_symbol': config.currency_symbol,
            'is_free_shipping': is_free,
        }
        return Response(data)


class ReturnPolicyView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ReturnPolicySerializer

    def get(self, request, *args, **kwargs):
        config = SiteConfiguration.get_active()
        if not config:
            return Response({'detail': 'Site configuration not found.'}, status=status.HTTP_404_NOT_FOUND)

        delivered_at = request.GET.get('delivered_at')
        days_remaining = None
        can_return = True

        if delivered_at:
            try:
                delivered_date = timezone.datetime.fromisoformat(delivered_at).replace(tzinfo=timezone.get_current_timezone())
                days_since = (timezone.now().date() - delivered_date.date()).days
                days_remaining = config.return_window_days - days_since
                if days_remaining < 0:
                    can_return = False
                    days_remaining = 0
            except (ValueError, TypeError):
                pass

        data = {
            'return_window_days': config.return_window_days,
            'auto_approve_returns': config.auto_approve_returns,
            'refund_processing_days': config.refund_processing_days,
            'can_return': can_return,
            'days_remaining': days_remaining,
        }
        return Response(data)


class PaymentMethodsView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PaymentMethodsSerializer

    def get(self, request, *args, **kwargs):
        from apps.payments.models import Payment
        methods = [
            {'id': 'cod', 'name': 'Cash On Delivery', 'icon': '💵', 'secure': True},
            {'id': 'stripe', 'name': 'Stripe', 'icon': '💳', 'secure': True},
            {'id': 'paypal', 'name': 'PayPal', 'icon': '🅿️', 'secure': True},
            {'id': 'jazzcash', 'name': 'JazzCash', 'icon': '📱', 'secure': True},
            {'id': 'easypaisa', 'name': 'EasyPaisa', 'icon': '📱', 'secure': True},
            {'id': 'bank_transfer', 'name': 'Bank Transfer', 'icon': '🏦', 'secure': True},
        ]
        data = {
            'methods': methods,
            'secure_payment': True,
        }
        return Response(data)


class SupportInfoView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SupportInfoSerializer

    def get(self, request, *args, **kwargs):
        config = SiteConfiguration.get_active()
        if not config:
            return Response({'detail': 'Site configuration not found.'}, status=status.HTTP_404_NOT_FOUND)

        is_open = True
        if not config.support_available_247:
            now = timezone.localtime().time()
            is_open = now.hour >= 9 and now.hour < 18

        data = {
            'available_247': config.support_available_247,
            'response_hours': config.support_response_hours,
            'sla_hours': config.ticket_sla_hours,
            'email': config.support_email or config.contact_email,
            'phone': config.support_phone or config.contact_phone,
            'is_open': is_open,
        }
        return Response(data)


class NewsletterSubscribeView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "Email is required."}, status=400)
        return Response({"message": "Subscription successful."}, status=201)
