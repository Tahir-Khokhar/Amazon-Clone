from django.contrib import admin
from .models import SearchQuery, SearchHistory, PopularSearch


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ['query', 'user', 'session_key', 'results_count', 'ip_address', 'created_at']
    list_filter = ['created_at']
    search_fields = ['query', 'user__username', 'session_key', 'ip_address']
    readonly_fields = ['created_at']


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'query', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'query']
    readonly_fields = ['created_at']


@admin.register(PopularSearch)
class PopularSearchAdmin(admin.ModelAdmin):
    list_display = ['query', 'count']
    search_fields = ['query']
