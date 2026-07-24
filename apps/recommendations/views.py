from rest_framework import generics, permissions

from .models import ProductRecommendation, UserPreference
from .serializers import ProductRecommendationSerializer, UserPreferenceSerializer


class ProductRecommendationsView(generics.ListAPIView):
    serializer_class = ProductRecommendationSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        product_slug = self.kwargs.get('product_slug')
        return ProductRecommendation.objects.filter(product__slug=product_slug).select_related('recommended_product').prefetch_related('recommended_product__images')[:10]


class UserRecommendationsView(generics.ListAPIView):
    serializer_class = ProductRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        from apps.recommendations.models import UserPreference
        user = self.request.user
        preferences = UserPreference.objects.filter(user=user).select_related('category').order_by('-score')[:5]
        categories = [p.category for p in preferences]
        return ProductRecommendation.objects.filter(
            product__category__in=categories
        ).select_related('recommended_product', 'product').prefetch_related('recommended_product__images')[:20]


class GenerateRecommendationsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        from apps.recommendations.models import ProductRecommendation, UserPreference
        from apps.products.models import Product
        from django.db.models import Count
        
        products = Product.objects.filter(is_active=True, status='published')
        count = 0
        
        for product in products:
            related = Product.objects.filter(
                category=product.category,
                is_active=True,
                status='published'
            ).exclude(pk=product.pk).annotate(
                review_count=Count('reviews')
            ).order_by('-average_rating', '-review_count')[:10]
            
            for idx, rec in enumerate(related):
                score = max(0, 100 - idx * 10)
                ProductRecommendation.objects.update_or_create(
                    product=product,
                    recommended_product=rec,
                    defaults={
                        'score': score,
                        'reason': 'Similar products in same category'
                    }
                )
                count += 1
        
        return Response({"message": f"Generated {count} recommendations."}, status=status.HTTP_200_OK)


class UserPreferenceListView(generics.ListAPIView):
    serializer_class = UserPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserPreference.objects.filter(user=self.request.user)
