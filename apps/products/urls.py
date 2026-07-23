from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ProductImageViewSet,
    ProductSpecificationViewSet,
    ProductVariantViewSet,
    ProductViewSet,
)

app_name = 'products'

# ---- Main Product Router ----
router = DefaultRouter()
router.register(r'', ProductViewSet, basename='product')

# ---- Nested Routers (for product sub-resources) ----
# These are registered separately to support nested URLs like:
#   /api/products/{product_slug}/images/
#   /api/products/{product_slug}/variants/
#   /api/products/{product_slug}/specifications/

nested_router_patterns = [
    path(
        '<slug:product_slug>/images/',
        ProductImageViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }),
        name='product-images-list',
    ),
    path(
        '<slug:product_slug>/images/<int:pk>/',
        ProductImageViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        name='product-images-detail',
    ),
    path(
        '<slug:product_slug>/variants/',
        ProductVariantViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }),
        name='product-variants-list',
    ),
    path(
        '<slug:product_slug>/variants/<int:pk>/',
        ProductVariantViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        name='product-variants-detail',
    ),
    path(
        '<slug:product_slug>/specifications/',
        ProductSpecificationViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }),
        name='product-specifications-list',
    ),
    path(
        '<slug:product_slug>/specifications/<int:pk>/',
        ProductSpecificationViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        name='product-specifications-detail',
    ),
]

urlpatterns = [
    # Main product endpoints (includes list, retrieve, create, update, partial_update, destroy, featured, latest, related, by_category, by_brand)
    path('', include(router.urls)),
    # Nested sub-resource endpoints
    path('', include(nested_router_patterns)),
]
