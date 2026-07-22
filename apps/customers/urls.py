from django.urls import path
from .views import (
    CustomerDashboardView,
    CustomerOrdersView,
    CustomerProfileView,
)

app_name = 'customers'

urlpatterns = [
    path('dashboard/', CustomerDashboardView.as_view(), name='dashboard'),
    path('orders/', CustomerOrdersView.as_view(), name='orders'),
    path('profile/', CustomerProfileView.as_view(), name='profile'),
]
