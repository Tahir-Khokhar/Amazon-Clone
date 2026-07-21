from django.urls import path
from .views import (
    PageViewCreateView,
    ProductViewCreateView,
    UserPageViewsView,
    PopularProductsView,
)

app_name = 'analytics'

urlpatterns = [
    path('page-view/', PageViewCreateView.as_view(), name='page-view'),
    path('product-view/', ProductViewCreateView.as_view(), name='product-view'),
    path('my-page-views/', UserPageViewsView.as_view(), name='my-page-views'),
    path('popular-products/', PopularProductsView.as_view(), name='popular-products'),
]
