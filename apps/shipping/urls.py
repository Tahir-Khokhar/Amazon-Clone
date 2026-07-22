from django.urls import path
from .views import (
    SellerDashboardView,
    SellerProductsView,
    SellerOrdersView,
    SellerCouponsView,
    SellerAnalyticsView,
)

app_name = 'sellers'

urlpatterns = [
    path('dashboard/', SellerDashboardView.as_view(), name='dashboard'),
    path('products/', SellerProductsView.as_view(), name='products'),
    path('orders/', SellerOrdersView.as_view(), name='orders'),
    path('coupons/', SellerCouponsView.as_view(), name='coupons'),
    path('analytics/', SellerAnalyticsView.as_view(), name='analytics'),
]
