from django.conf import settings
from django.db import models


class BrowsingHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='browsing_history')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='viewed_by')
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']
        indexes = [
            models.Index(fields=['user', '-viewed_at']),
        ]

    def __str__(self):
        return f"{self.user.username} viewed {self.product.name}"
