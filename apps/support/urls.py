from django.urls import path
from .views import (
    FAQListView,
    SupportTicketListCreateView,
    SupportTicketDetailView,
    TicketMessageCreateView,
)

app_name = 'support'

urlpatterns = [
    path('faqs/', FAQListView.as_view(), name='faq-list'),
    path('tickets/', SupportTicketListCreateView.as_view(), name='ticket-list-create'),
    path('tickets/<int:pk>/', SupportTicketDetailView.as_view(), name='ticket-detail'),
    path('tickets/<int:pk>/message/', TicketMessageCreateView.as_view(), name='ticket-message-create'),
]
