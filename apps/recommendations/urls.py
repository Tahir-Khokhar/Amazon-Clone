from django.urls import path
from rest_framework.response import Response
from .views import (
    ProductRecommendationsView,
    UserRecommendationsView,
    GenerateRecommendationsView,
    UserPreferenceListView,
)

app_name = 'recommendations'

urlpatterns = [
    path('products/<slug:product_slug>/', ProductRecommendationsView.as_view(), name='product-recommendations'),
    path('my/', UserRecommendationsView.as_view(), name='user-recommendations'),
    path('generate/', GenerateRecommendationsView.as_view(), name='generate-recommendations'),
    path('preferences/', UserPreferenceListView.as_view(), name='user-preferences'),
]
