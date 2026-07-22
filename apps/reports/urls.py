from django.urls import path
from .views import SalesReportView, TopProductsView, TopCategoriesView

app_name = 'reports'

urlpatterns = [
    path('sales/', SalesReportView.as_view(), name='sales-report'),
    path('top-products/', TopProductsView.as_view(), name='top-products'),
    path('top-categories/', TopCategoriesView.as_view(), name='top-categories'),
]
