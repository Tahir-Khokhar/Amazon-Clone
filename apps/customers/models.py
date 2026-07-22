from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class CustomerProfile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_profile')
    total_orders = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    wishlist_count = models.IntegerField(default=0)
    loyalty_points = models.IntegerField(default=0)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Customer Profile"
