from django.contrib import admin
from .models import ProductRecommendation, UserPreference


@admin.register(ProductRecommendation)
class ProductRecommendationAdmin(admin.ModelAdmin):
    list_display = ['product', 'recommended_product', 'score', 'created_at']
    list_filter = ['created_at']
    search_fields = ['product__name', 'recommended_product__name']


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'score', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['user__username', 'category__name']
