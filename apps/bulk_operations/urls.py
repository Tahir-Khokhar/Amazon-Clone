from django.urls import path
from .views import (
    ImportJobListView,
    ImportJobDetailView,
    ImportCreateView,
    ExportProductsView,
)

app_name = 'bulk_operations'

urlpatterns = [
    path('imports/', ImportJobListView.as_view(), name='import-list'),
    path('imports/<int:pk>/', ImportJobDetailView.as_view(), name='import-detail'),
    path('import/', ImportCreateView.as_view(), name='import-create'),
    path('export/products/', ExportProductsView.as_view(), name='export-products'),
]
