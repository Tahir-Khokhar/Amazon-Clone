from django.db import models
from django.conf import settings


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=100, default='Amazon Clone')
    site_description = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)

    free_shipping_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=50.00, help_text='Minimum order amount for free shipping')
    standard_shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=5.00, help_text='Standard shipping cost')
    express_shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=15.00, help_text='Express shipping cost')

    return_window_days = models.IntegerField(default=30, help_text='Number of days after delivery for returns')
    auto_approve_returns = models.BooleanField(default=False, help_text='Automatically approve return requests')
    refund_processing_days = models.IntegerField(default=7, help_text='Business days to process refund')

    support_email = models.EmailField(blank=True)
    support_phone = models.CharField(max_length=20, blank=True)
    support_available_247 = models.BooleanField(default=True, help_text='Is support available 24/7')
    support_response_hours = models.CharField(max_length=100, default='24/7', help_text='Support availability hours')
    ticket_sla_hours = models.IntegerField(default=24, help_text='SLA in hours for ticket response')

    currency = models.CharField(max_length=10, default='USD')
    currency_symbol = models.CharField(max_length=5, default='$')
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text='Default tax rate percentage')

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Configuration'
        verbose_name_plural = 'Site Configuration'

    def __str__(self):
        return self.site_name

    @classmethod
    def get_active(cls):
        return cls.objects.filter(is_active=True).first() or cls.objects.first()


class Subscription(TimeStampedModel):
    PLAN_CHOICES = (
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='subscriptions')
    email = models.EmailField()
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='monthly')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_data = models.JSONField(default=dict, blank=True)
    starts_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} - {self.plan} ({self.status})"
