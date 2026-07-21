from django.urls import path
from .views import BrandListView, BrandDetailView, BrandCreateView

app_name = 'brands'

urlpatterns = [
    path('', BrandListView.as_view(), name='brand-list'),
    path('<slug:slug>/', BrandDetailView.as_view(), name='brand-detail'),
    path('create/', BrandCreateView.as_view(), name='brand-create'),
]
