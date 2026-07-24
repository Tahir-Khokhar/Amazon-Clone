from django.conf import settings
from django.db import models


class ProductRecommendation(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='recommendations')
    recommended_product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='recommended_in')
    score = models.FloatField(default=0, help_text="Recommendation score (higher = better match)")
    reason = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score', '-created_at']
        unique_together = ('product', 'recommended_product')

    def __str__(self):
        return f"{self.product.name} -> {self.recommended_product.name}"


class UserPreference(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preferences')
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE, related_name='user_preferences')
    score = models.FloatField(default=0, help_text="Preference score (higher = more interest)")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-score']
        unique_together = ('user', 'category')

    def __str__(self):
        return f"{self.user.username} - {self.category.name}"
