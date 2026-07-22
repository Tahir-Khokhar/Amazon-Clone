from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category
from .serializers import CategorySerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["parent", "is_active"]


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        from rest_framework.permissions import SAFE_METHODS
        if self.request.method in SAFE_METHODS:
            return [permissions.AllowAny()]
        user = self.request.user
        if user.is_authenticated and (user.is_staff or user.role == "seller"):
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


class CategoryTreeView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Category.objects.filter(parent__isnull=True, is_active=True)
