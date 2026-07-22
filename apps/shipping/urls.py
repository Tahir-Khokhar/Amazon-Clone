from django.urls import path
from .views import (
    ShippingMethodListView,
    ShippingAddressListCreateView,
    ShipmentDetailView,
)

app_name = 'shipping'

urlpatterns = [
    path('methods/', ShippingMethodListView.as_view(), name='shipping-methods'),
    path('addresses/', ShippingAddressListCreateView.as_view(), name='shipping-address-list-create'),
    path('shipment/<int:order_id>/', ShipmentDetailView.as_view(), name='shipment-detail'),
]
