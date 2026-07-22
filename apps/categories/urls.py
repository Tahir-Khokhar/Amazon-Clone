from django.urls import path
from .views import CategoryListView, CategoryDetailView, CategoryTreeView, CategoryCreateView

app_name = 'categories'

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    path('tree/', CategoryTreeView.as_view(), name='category-tree'),
    path('create/', CategoryCreateView.as_view(), name='category-create'),
]
