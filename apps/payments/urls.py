from django.urls import path
from .views import (
    PaymentListView,
    PaymentDetailView,
    PaymentInitiateView,
    PaymentWebhookView,
)

app_name = 'payments'

urlpatterns = [
    path('', PaymentListView.as_view(), name='payment-list'),
    path('<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
    path('initiate/', PaymentInitiateView.as_view(), name='payment-initiate'),
    path('webhook/', PaymentWebhookView.as_view(), name='payment-webhook'),
]
