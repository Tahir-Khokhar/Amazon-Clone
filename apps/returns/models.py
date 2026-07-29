from django.conf import settings
from django.db import models


class ReturnRequest(models.Model):
    RETURN_TYPE_CHOICES = (
        ('return', 'Return'),
        ('replacement', 'Replacement'),
        ('refund', 'Refund'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    REASON_CHOICES = (
        ('defective', 'Defective/Damaged'),
        ('wrong_item', 'Wrong Item'),
        ('not_as_described', 'Not As Described'),
        ('changed_mind', 'Changed Mind'),
        ('size_issue', 'Size Issue'),
        ('other', 'Other'),
    )

    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='returns')
    order_item = models.ForeignKey('orders.OrderItem', on_delete=models.CASCADE, related_name='returns')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='return_requests')
    return_type = models.CharField(max_length=20, choices=RETURN_TYPE_CHOICES, default='return')
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    description = models.TextField()
    images = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_note = models.TextField(blank=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Return {self.id} - {self.order.order_number}"
