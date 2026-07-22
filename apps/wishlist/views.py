from django.urls import path
from .views import (
    WishlistView,
    WishlistAddView,
    WishlistRemoveView,
    WishlistMoveToCartView,
)

app_name = 'wishlist'

urlpatterns = [
    path('', WishlistView.as_view(), name='wishlist'),
    path('add/', WishlistAddView.as_view(), name='wishlist-add'),
    path('<int:pk>/remove/', WishlistRemoveView.as_view(), name='wishlist-remove'),
    path('<int:pk>/move-to-cart/', WishlistMoveToCartView.as_view(), name='wishlist-move-to-cart'),
]
