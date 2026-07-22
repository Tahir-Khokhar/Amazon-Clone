from django.conf import settings
from django.db import models


class Coupon(models.Model):
    COUPON_TYPE_CHOICES = (
        ('flat', 'Flat Discount'),
        ('percentage', 'Percentage Discount'),
        ('free_shipping', 'Free Shipping'),
    )
    code = models.CharField(max_length=50, unique=True)
    coupon_type = models.CharField(max_length=20, choices=COUPON_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    usage_limit = models.IntegerField(default=0, help_text="0 = unlimited")
    used_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-valid_until']

    def __str__(self):
        return self.code


class CouponUsage(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, null=True, blank=True)
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('coupon', 'user', 'order')

    def __str__(self):
        return f"{self.coupon.code} - {self.user}"
