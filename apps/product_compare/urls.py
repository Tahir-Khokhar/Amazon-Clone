from django.urls import path
from .views import (
    CompareListView,
    AddToCompareView,
    RemoveFromCompareView,
    ClearCompareView,
)

app_name = 'product_compare'

urlpatterns = [
    path('', CompareListView.as_view(), name='compare-list'),
    path('add/<int:product_id>/', AddToCompareView.as_view(), name='add-to-compare'),
    path('remove/<int:product_id>/', RemoveFromCompareView.as_view(), name='remove-from-compare'),
    path('clear/', ClearCompareView.as_view(), name='clear-compare'),
]
