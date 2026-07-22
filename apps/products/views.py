from django.db.models import Q
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, ProductVariant
from .serializers import ProductListSerializer, ProductDetailSerializer, ProductCreateSerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category", "brand", "seller", "is_featured", "is_active"]
    search_fields = ["name", "description", "short_description"]
    ordering_fields = ["price", "created_at", "views_count", "sales_count"]
    ordering = ["-created_at"]


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        user = self.request.user
        if user.is_staff or user.role in ["seller", "admin"]:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class ProductUpdateView(generics.UpdateAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.role == "admin":
            return Product.objects.all()
        return Product.objects.filter(seller=user)


class ProductDeleteView(generics.DestroyAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.role == "admin":
            return Product.objects.all()
        return Product.objects.filter(seller=user)


class ProductSearchView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        query = self.request.query_params.get("q", "")
        if query:
            return Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query) | Q(sku__icontains=query),
                is_active=True,
            )
        return Product.objects.none()


class FeaturedProductsView(generics.ListAPIView):
    queryset = Product.objects.filter(is_featured=True, is_active=True)
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class RelatedProductsView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        try:
            product = Product.objects.get(slug=slug, is_active=True)
        except Product.DoesNotExist:
            return Product.objects.none()
        return Product.objects.filter(
            Q(category=product.category) | Q(brand=product.brand),
            is_active=True,
        ).exclude(pk=product.pk)[:8]
