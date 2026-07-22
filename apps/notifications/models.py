from django.conf import settings
from django.db import models


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = (
        ('order', 'Order Update'),
        ('offer', 'Offer'),
        ('wishlist', 'Wishlist Alert'),
        ('account', 'Account'),
        ('support', 'Support'),
    )
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient} - {self.title}"
