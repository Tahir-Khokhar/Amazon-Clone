import django_filters
from django.db.models import Q

from .models import Product, ProductStatus


class ProductFilter(django_filters.FilterSet):
    """
    Advanced filter set for the Product model.

    Supports:
      - Search by name, description, SKU
      - Filter by category (id or slug)
      - Filter by brand (id or slug)
      - Filter by price range (min / max)
      - Filter by rating (min)
      - Filter by availability (in-stock only)
      - Ordering by price, created_at, average_rating
    """

    # --- Search ---
    search = django_filters.CharFilter(method='filter_search')

    # --- Category ---
    category = django_filters.NumberFilter(field_name='category__id')
    category_slug = django_filters.CharFilter(field_name='category__slug')

    # --- Brand ---
    brand = django_filters.NumberFilter(field_name='brand__id')
    brand_slug = django_filters.CharFilter(field_name='brand__slug')

    # --- Price range ---
    price_min = django_filters.NumberFilter(
        field_name='price', lookup_expr='gte'
    )
    price_max = django_filters.NumberFilter(
        field_name='price', lookup_expr='lte'
    )

    # --- Discount price range ---
    discount_price_min = django_filters.NumberFilter(
        field_name='discount_price', lookup_expr='gte'
    )
    discount_price_max = django_filters.NumberFilter(
        field_name='discount_price', lookup_expr='lte'
    )

    # --- Rating ---
    rating_min = django_filters.NumberFilter(
        field_name='average_rating', lookup_expr='gte'
    )

    # --- Availability (in-stock only) ---
    in_stock = django_filters.BooleanFilter(method='filter_in_stock')

    # --- Featured ---
    is_featured = django_filters.BooleanFilter(field_name='is_featured')

    # --- Status ---
    status = django_filters.ChoiceFilter(choices=ProductStatus.choices)

    class Meta:
        model = Product
        fields = [
            'search', 'category', 'category_slug',
            'brand', 'brand_slug',
            'price_min', 'price_max',
            'discount_price_min', 'discount_price_max',
            'rating_min', 'in_stock',
            'is_featured', 'status',
        ]

    @staticmethod
    def filter_search(queryset, name, value):
        """Search across name, short_description, full_description, and SKU."""
        if not value:
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(short_description__icontains=value) |
            Q(full_description__icontains=value) |
            Q(description__icontains=value) |
            Q(sku__icontains=value) |
            Q(brand__name__icontains=value) |
            Q(category__name__icontains=value)
        )

    @staticmethod
    def filter_in_stock(queryset, name, value):
        """Filter to show only products with stock > 0."""
        if value:
            return queryset.filter(stock__gt=0)
        return queryset

