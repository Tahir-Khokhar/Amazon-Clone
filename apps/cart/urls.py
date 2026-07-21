from django.urls import path
from .views import (
    CartListView,
    CartDetailView,
    CartItemCreateView,
    CartItemUpdateView,
    CartItemDeleteView,
)

app_name = 'cart'

urlpatterns = [
    path('', CartListView.as_view(), name='cart'),
    path('add/', CartItemCreateView.as_view(), name='cart-add'),
    path('<int:pk>/update/', CartItemUpdateView.as_view(), name='cart-update'),
    path('<int:pk>/remove/', CartItemDeleteView.as_view(), name='cart-remove'),
]
