from django.db import models


class SalesReport(models.Model):
    date = models.DateField()
    total_orders = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_products_sold = models.IntegerField(default=0)
    total_customers = models.IntegerField(default=0)

    class Meta:
        unique_together = ('date',)
        ordering = ['-date']

    def __str__(self):
        return f"Sales Report - {self.date}"


class TopProduct(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    total_sales = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_orders = models.IntegerField(default=0)
    period_start = models.DateField()
    period_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - Top Product"


class TopCategory(models.Model):
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE)
    total_sales = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    period_start = models.DateField()
    period_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name} - Top Category"
