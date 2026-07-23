from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import filters, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import ProductFilter
from .models import (
    Product,
    ProductImage,
    ProductSpecification,
    ProductStatus,
    ProductVariant,
)
from .serializers import (
    ProductCreateUpdateSerializer,
    ProductDetailSerializer,
    ProductImageSerializer,
    ProductListSerializer,
    ProductSpecificationSerializer,
    ProductVariantSerializer,
)


# ============================================================================
# Custom Pagination
# ============================================================================

class ProductPagination(PageNumberPagination):
    """Default pagination for product listing endpoints."""

    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


# ============================================================================
# Permissions
# ============================================================================

def _is_admin_or_staff(user):
    """Check if the user is an admin, staff, or has admin role."""
    return bool(user and (user.is_staff or user.is_superuser or getattr(user, 'role', None) == 'admin'))


class IsAdminUserForWrite(permissions.BasePermission):
    """
    Custom permission:
      - Anyone can read (safe methods).
      - Only admin / staff can write (POST, PUT, PATCH, DELETE).
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and _is_admin_or_staff(request.user))

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and _is_admin_or_staff(request.user))


# ============================================================================
# Product ViewSet
# ============================================================================

@extend_schema_view(
    list=extend_schema(
        summary="List Products",
        description="Retrieve a paginated list of active products with filtering, search, and ordering.",
        parameters=[
            OpenApiParameter(name='search', description='Search term', required=False, type=str),
            OpenApiParameter(name='category', description='Category ID', required=False, type=int),
            OpenApiParameter(name='brand', description='Brand ID', required=False, type=int),
            OpenApiParameter(name='price_min', description='Minimum price', required=False, type=float),
            OpenApiParameter(name='price_max', description='Maximum price', required=False, type=float),
            OpenApiParameter(name='rating_min', description='Minimum average rating', required=False, type=float),
            OpenApiParameter(name='in_stock', description='Only in-stock items', required=False, type=bool),
            OpenApiParameter(name='ordering', description='Order by price, -price, created_at, -created_at, average_rating, -average_rating', required=False, type=str),
        ],
        responses={200: ProductListSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Product Detail",
        description="Retrieve full details of a single product by its slug.",
        responses={200: ProductDetailSerializer},
    ),
    create=extend_schema(
        summary="Create Product",
        description="Create a new product. Admin-only.",
        request=ProductCreateUpdateSerializer,
        responses={201: ProductCreateUpdateSerializer},
    ),
    update=extend_schema(
        summary="Update Product",
        description="Fully update an existing product. Admin-only.",
        request=ProductCreateUpdateSerializer,
        responses={200: ProductCreateUpdateSerializer},
    ),
    partial_update=extend_schema(
        summary="Partial Update Product",
        description="Partially update an existing product. Admin-only.",
        request=ProductCreateUpdateSerializer,
        responses={200: ProductCreateUpdateSerializer},
    ),
    destroy=extend_schema(
        summary="Delete Product",
        description="Delete a product. Admin-only.",
        responses={204: None},
    ),
)
class ProductViewSet(ModelViewSet):
    """
    ViewSet for Product CRUD operations and custom actions.

    **Public endpoints (no auth required):**
      - GET /api/products/ — List
      - GET /api/products/{slug}/ — Detail
      - GET /api/products/featured/ — Featured
      - GET /api/products/latest/ — Latest
      - GET /api/products/{slug}/related/ — Related
      - GET /api/products/by_category/{category_slug}/ — By Category
      - GET /api/products/by_brand/{brand_slug}/ — By Brand

    **Admin-only endpoints (auth required):**
      - POST /api/products/create/ — Create
      - PUT /api/products/{slug}/update/ — Update
      - PATCH /api/products/{slug}/update/ — Partial Update
      - DELETE /api/products/{slug}/delete/ — Delete
    """

    lookup_field = 'slug'
    pagination_class = ProductPagination
    permission_classes = [IsAdminUserForWrite]

    # Default filter backends (DRF global defaults also apply)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ProductFilter
    search_fields = [
        'name', 'short_description', 'full_description',
        'description', 'sku', 'brand__name', 'category__name',
    ]
    ordering_fields = [
        'price', 'created_at', 'average_rating',
        'views_count', 'sales_count',
    ]
    ordering = ['-created_at']

    # ------ Serializer selection ------

    def get_serializer_class(self):
        """Select the appropriate serializer based on the action."""
        if self.action == 'list':
            return ProductListSerializer
        if self.action == 'retrieve':
            return ProductDetailSerializer
        # create, update, partial_update
        return ProductCreateUpdateSerializer

    # ------ Queryset with optimization ------

    def get_queryset(self):
        """
        Return optimized queryset.
        - Detail view: eager-load all relations.
        - List/custom: select_related on FK fields, prefetch images for primary_image.
        """
        qs = Product.objects.select_related('brand', 'category', 'seller')

        # Detail view needs full relations
        if self.action == 'retrieve':
            return qs.prefetch_related(
                'images', 'variants', 'specifications',
                'attribute_values__attribute', 'tags',
            )

        # List view: only prefetch images for primary_image
        if self.action == 'list':
            return qs.prefetch_related('images').filter(is_active=True)

        # Custom actions: featured, latest, related, by_category, by_brand
        return qs.prefetch_related('images')

    # ------ Create override ------

    def perform_create(self, serializer):
        """Automatically assign the seller to the current user."""
        serializer.save(seller=self.request.user)

    # ------ Custom Actions ------

    @extend_schema(
        summary="Featured Products",
        description="Retrieve a list of featured products.",
        responses={200: ProductListSerializer(many=True)},
    )
    @action(detail=False, methods=['get'], url_path='featured')
    def featured(self, request):
        """Return all featured products."""
        queryset = (
            Product.objects.select_related('brand', 'category')
            .prefetch_related('images')
            .filter(is_featured=True, is_active=True, status=ProductStatus.PUBLISHED)
        )
        # Use pagination for consistency, or disable it via no pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = ProductListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @extend_schema(
        summary="Latest Products",
        description="Retrieve the latest products ordered by creation date.",
        responses={200: ProductListSerializer(many=True)},
    )
    @action(detail=False, methods=['get'], url_path='latest')
    def latest(self, request):
        """Return the 12 most recently created products."""
        queryset = (
            Product.objects.select_related('brand', 'category')
            .prefetch_related('images')
            .filter(is_active=True, status=ProductStatus.PUBLISHED)
            .order_by('-created_at')[:12]
        )
        serializer = ProductListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @extend_schema(
        summary="Related Products",
        description="Retrieve products related to a given product (same category or brand).",
        responses={200: ProductListSerializer(many=True)},
    )
    @action(detail=True, methods=['get'], url_path='related')
    def related(self, request, slug=None):
        """Return up to 8 related products (same category or brand)."""
        try:
            product = Product.objects.get(slug=slug, is_active=True)
        except Product.DoesNotExist:
            raise NotFound("Product not found.")

        queryset = (
            Product.objects.select_related('brand', 'category')
            .prefetch_related('images')
            .filter(
                Q(category=product.category) | Q(brand=product.brand),
                is_active=True,
                status=ProductStatus.PUBLISHED,
            )
            .exclude(pk=product.pk)
            .order_by('-created_at')[:8]
        )
        serializer = ProductListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @extend_schema(
        summary="Products by Category",
        description="Retrieve all products belonging to a specific category (by slug).",
        responses={200: ProductListSerializer(many=True)},
    )
    @action(detail=False, methods=['get'], url_path='by-category/(?P<category_slug>[^/.]+)')
    def by_category(self, request, category_slug=None):
        """Return products filtered by category slug."""
        queryset = (
            Product.objects.select_related('brand', 'category')
            .prefetch_related('images')
            .filter(
                category__slug=category_slug,
                is_active=True,
                status=ProductStatus.PUBLISHED,
            )
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = ProductListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @extend_schema(
        summary="Products by Brand",
        description="Retrieve all products belonging to a specific brand (by slug).",
        responses={200: ProductListSerializer(many=True)},
    )
    @action(detail=False, methods=['get'], url_path='by-brand/(?P<brand_slug>[^/.]+)')
    def by_brand(self, request, brand_slug=None):
        """Return products filtered by brand slug."""
        queryset = (
            Product.objects.select_related('brand', 'category')
            .prefetch_related('images')
            .filter(
                brand__slug=brand_slug,
                is_active=True,
                status=ProductStatus.PUBLISHED,
            )
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = ProductListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


# ============================================================================
# Nested Model ViewSets (for create/update individual sub-resources)
# ============================================================================

@extend_schema_view(
    list=extend_schema(summary="List Product Images", responses={200: ProductImageSerializer(many=True)}),
    create=extend_schema(summary="Add Product Image", request=ProductImageSerializer, responses={201: ProductImageSerializer}),
    destroy=extend_schema(summary="Delete Product Image", responses={204: None}),
)
class ProductImageViewSet(ModelViewSet):
    """CRUD for product images (admin-only for write)."""

    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminUserForWrite]

    def get_queryset(self):
        return ProductImage.objects.filter(product__slug=self.kwargs.get('product_slug'))

    def perform_create(self, serializer):
        product = Product.objects.get(slug=self.kwargs.get('product_slug'))
        serializer.save(product=product)


@extend_schema_view(
    list=extend_schema(summary="List Product Variants", responses={200: ProductVariantSerializer(many=True)}),
    create=extend_schema(summary="Add Product Variant", request=ProductVariantSerializer, responses={201: ProductVariantSerializer}),
    destroy=extend_schema(summary="Delete Product Variant", responses={204: None}),
)
class ProductVariantViewSet(ModelViewSet):
    """CRUD for product variants (admin-only for write)."""

    serializer_class = ProductVariantSerializer
    permission_classes = [IsAdminUserForWrite]

    def get_queryset(self):
        return ProductVariant.objects.filter(product__slug=self.kwargs.get('product_slug'))

    def perform_create(self, serializer):
        product = Product.objects.get(slug=self.kwargs.get('product_slug'))
        serializer.save(product=product)


@extend_schema_view(
    list=extend_schema(summary="List Product Specifications", responses={200: ProductSpecificationSerializer(many=True)}),
    create=extend_schema(summary="Add Product Specification", request=ProductSpecificationSerializer, responses={201: ProductSpecificationSerializer}),
    destroy=extend_schema(summary="Delete Product Specification", responses={204: None}),
)
class ProductSpecificationViewSet(ModelViewSet):
    """CRUD for product specifications (admin-only for write)."""

    serializer_class = ProductSpecificationSerializer
    permission_classes = [IsAdminUserForWrite]

    def get_queryset(self):
        return ProductSpecification.objects.filter(product__slug=self.kwargs.get('product_slug'))

    def perform_create(self, serializer):
        product = Product.objects.get(slug=self.kwargs.get('product_slug'))
        serializer.save(product=product)
