from django.urls import path
from .views import BrowsingHistoryListView, BrowsingHistoryClearView

app_name = 'browsing_history'

urlpatterns = [
    path('', BrowsingHistoryListView.as_view(), name='history-list'),
    path('clear/', BrowsingHistoryClearView.as_view(), name='history-clear'),
]
