from django.urls import path
from .views import (
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderCancelView,
    AdminOrderListView,
    SellerOrderListView,
    DeliveryOrderListView,
)

app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('<int:pk>/cancel/', OrderCancelView.as_view(), name='order-cancel'),
    path('admin/all/', AdminOrderListView.as_view(), name='admin-order-list'),
    path('seller/my/', SellerOrderListView.as_view(), name='seller-order-list'),
    path('delivery/assigned/', DeliveryOrderListView.as_view(), name='delivery-order-list'),
]
