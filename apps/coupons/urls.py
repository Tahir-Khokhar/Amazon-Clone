from django.urls import path
from .views import CouponListView, CouponDetailView, CouponValidateView, CouponCreateView

app_name = 'coupons'

urlpatterns = [
    path('', CouponListView.as_view(), name='coupon-list'),
    path('<int:pk>/', CouponDetailView.as_view(), name='coupon-detail'),
    path('validate/', CouponValidateView.as_view(), name='coupon-validate'),
    path('create/', CouponCreateView.as_view(), name='coupon-create'),
]
