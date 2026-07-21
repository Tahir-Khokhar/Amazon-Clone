from django.urls import path
from .views import AddressListCreateView, AddressDetailView

app_name = 'addresses'

urlpatterns = [
    path('', AddressListCreateView.as_view(), name='address-list-create'),
    path('<int:pk>/', AddressDetailView.as_view(), name='address-detail'),
]
