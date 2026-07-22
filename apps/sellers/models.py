from django.conf import settings
from django.db import models


class SearchQuery(models.Model):
    query = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True)
    results_count = models.IntegerField(default=0)
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query


class SearchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='search_history')
    query = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.query


class PopularSearch(models.Model):
    query = models.CharField(max_length=200, unique=True)
    count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-count']

    def __str__(self):
        return self.query
