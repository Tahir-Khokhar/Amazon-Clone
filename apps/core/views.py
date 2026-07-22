from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({"status": "ok"}, status=200)


class APIRootView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        endpoints = {
            "health": "/api/health/",
            "accounts": "/api/accounts/",
            "products": "/api/products/",
            "categories": "/api/categories/",
            "brands": "/api/brands/",
            "cart": "/api/cart/",
            "orders": "/api/orders/",
            "payments": "/api/payments/",
            "wishlist": "/api/wishlist/",
            "reviews": "/api/reviews/",
            "coupons": "/api/coupons/",
            "shipping": "/api/shipping/",
            "notifications": "/api/notifications/",
            "search": "/api/search/",
            "sellers": "/api/sellers/",
            "customers": "/api/customers/",
            "dashboard": "/api/dashboard/",
            "reports": "/api/reports/",
            "analytics": "/api/analytics/",
            "support": "/api/support/",
        }
        return Response(endpoints, status=200)
