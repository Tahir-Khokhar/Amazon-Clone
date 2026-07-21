from django.conf import settings
from rest_framework import generics, permissions

from .models import PageView, ProductView
from .serializers import PageViewSerializer, ProductViewSerializer


class PageViewCreateView(generics.CreateAPIView):
    serializer_class = PageViewSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        ip_address = self.request.META.get("REMOTE_ADDR", "")
        user_agent = self.request.META.get("HTTP_USER_AGENT", "")
        session_key = self.request.session.session_key or ""
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(
            ip_address=ip_address,
            user_agent=user_agent,
            session_key=session_key,
            user=user,
        )


class ProductViewCreateView(generics.CreateAPIView):
    serializer_class = ProductViewSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        ip_address = self.request.META.get("REMOTE_ADDR", "")
        session_key = self.request.session.session_key or ""
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(ip_address=ip_address, session_key=session_key, user=user)


class UserPageViewsView(generics.ListAPIView):
    serializer_class = PageViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PageView.objects.filter(user=self.request.user).order_by("-created_at")


class PopularProductsView(generics.ListAPIView):
    serializer_class = ProductViewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        from django.db.models import Count
        return ProductView.objects.values("product").annotate(
            view_count=Count("id")
        ).order_by("-view_count")[:10]
