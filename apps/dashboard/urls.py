from django.urls import path
from .views import AdminDashboardView, SellerDashboardView

app_name = 'dashboard'

urlpatterns = [
    path('admin/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('seller/', SellerDashboardView.as_view(), name='seller-dashboard'),
]
