from django.db import models


class DashboardStat(models.Model):
    date = models.DateField()
    total_orders = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_users = models.IntegerField(default=0)
    total_products = models.IntegerField(default=0)
    new_orders = models.IntegerField(default=0)
    new_users = models.IntegerField(default=0)

    class Meta:
        unique_together = ('date',)
        ordering = ['-date']

    def __str__(self):
        return f"Stats for {self.date}"
