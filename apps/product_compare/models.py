from django.conf import settings
from django.db import models


class CompareList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='compare_list')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Compare List - {self.user.username}"


class CompareItem(models.Model):
    compare_list = models.ForeignKey(CompareList, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('compare_list', 'product')
        ordering = ['created_at']

    def __str__(self):
        return f"{self.product.name} in {self.compare_list}"
