from django.urls import path
from .views import (
    ReturnRequestListView,
    ReturnRequestDetailView,
    ReturnRequestCreateView,
    ReturnRequestAdminUpdateView,
)

app_name = 'returns'

urlpatterns = [
    path('', ReturnRequestListView.as_view(), name='return-list'),
    path('create/', ReturnRequestCreateView.as_view(), name='return-create'),
    path('<int:pk>/', ReturnRequestDetailView.as_view(), name='return-detail'),
    path('<int:pk>/admin-update/', ReturnRequestAdminUpdateView.as_view(), name='return-admin-update'),
]
