from django.urls import path
from .views import SearchView, SearchHistoryView, PopularSearchesView, AutocompleteView

app_name = 'search'

urlpatterns = [
    path('', SearchView.as_view(), name='search'),
    path('history/', SearchHistoryView.as_view(), name='search-history'),
    path('popular/', PopularSearchesView.as_view(), name='popular-searches'),
    path('autocomplete/', AutocompleteView.as_view(), name='autocomplete'),
]
