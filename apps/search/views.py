from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.products.models import Product
from apps.categories.models import Category
from apps.brands.models import Brand
from .models import SearchQuery, SearchHistory, PopularSearch
from .serializers import SearchQuerySerializer, SearchHistorySerializer, PopularSearchSerializer
from apps.products.serializers import ProductListSerializer
from apps.categories.serializers import CategorySerializer
from apps.brands.serializers import BrandSerializer


class SearchView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SearchQuerySerializer

    def get(self, request, *args, **kwargs):
        query = request.query_params.get("q", "")
        category_id = request.query_params.get("category")
        brand_id = request.query_params.get("brand")
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")

        products = Product.objects.filter(is_active=True)
        categories = Category.objects.filter(is_active=True)
        brands = Brand.objects.filter(is_active=True)

        if query:
            products = products.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
            categories = categories.filter(name__icontains=query)
            brands = brands.filter(name__icontains=query)
        if category_id:
            products = products.filter(category_id=category_id)
        if brand_id:
            products = products.filter(brand_id=brand_id)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        if query:
            SearchQuery.objects.create(
                query=query,
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key or "",
                ip_address=request.META.get("REMOTE_ADDR", ""),
                results_count=products.count(),
            )
            if request.user.is_authenticated:
                SearchHistory.objects.create(user=request.user, query=query)
            else:
                popular_search, _ = PopularSearch.objects.get_or_create(query=query)
                popular_search.count += 1
                popular_search.save()

        return Response(
            {
                "products": ProductListSerializer(products, many=True).data,
                "categories": CategorySerializer(categories, many=True).data,
                "brands": BrandSerializer(brands, many=True).data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class SearchHistoryView(generics.ListAPIView):
    serializer_class = SearchHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SearchHistory.objects.filter(user=self.request.user)


class PopularSearchesView(generics.ListAPIView):
    queryset = PopularSearch.objects.all()[:10]
    serializer_class = PopularSearchSerializer
    permission_classes = [permissions.AllowAny]


class AutocompleteView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        query = request.query_params.get("q", "")
        suggestions = []
        if query:
            suggestions = list(
                Product.objects.filter(name__icontains=query, is_active=True)
                .values_list("name", flat=True)[:5]
            )
        return Response({"suggestions": suggestions}, status=status.HTTP_200_OK)
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.products.models import Product
from apps.categories.models import Category
from apps.brands.models import Brand
from .models import SearchQuery, SearchHistory, PopularSearch
from .serializers import SearchQuerySerializer, SearchHistorySerializer, PopularSearchSerializer
from apps.products.serializers import ProductListSerializer
from apps.categories.serializers import CategorySerializer
from apps.brands.serializers import BrandSerializer


class SearchView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SearchQuerySerializer

    def get(self, request, *args, **kwargs):
        query = request.query_params.get("q", "")
        category_id = request.query_params.get("category")
        brand_id = request.query_params.get("brand")
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")

        products = Product.objects.filter(is_active=True)
        categories = Category.objects.filter(is_active=True)
        brands = Brand.objects.filter(is_active=True)

        if query:
            products = products.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
            categories = categories.filter(name__icontains=query)
            brands = brands.filter(name__icontains=query)
        if category_id:
            products = products.filter(category_id=category_id)
        if brand_id:
            products = products.filter(brand_id=brand_id)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        if query:
            SearchQuery.objects.create(
                query=query,
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key or "",
                ip_address=request.META.get("REMOTE_ADDR", ""),
                results_count=products.count(),
            )
            if request.user.is_authenticated:
                SearchHistory.objects.create(user=request.user, query=query)
            else:
                popular_search, _ = PopularSearch.objects.get_or_create(query=query)
                popular_search.count += 1
                popular_search.save()

        return Response(
            {
                "products": ProductListSerializer(products, many=True).data,
                "categories": CategorySerializer(categories, many=True).data,
                "brands": BrandSerializer(brands, many=True).data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class SearchHistoryView(generics.ListAPIView):
    serializer_class = SearchHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SearchHistory.objects.filter(user=self.request.user)


class PopularSearchesView(generics.ListAPIView):
    queryset = PopularSearch.objects.all()[:10]
    serializer_class = PopularSearchSerializer
    permission_classes = [permissions.AllowAny]


class AutocompleteView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        query = request.query_params.get("q", "")
        suggestions = []
        if query:
            suggestions = list(
                Product.objects.filter(name__icontains=query, is_active=True)
                .values_list("name", flat=True)[:5]
            )
        return Response({"suggestions": suggestions}, status=status.HTTP_200_OK)
