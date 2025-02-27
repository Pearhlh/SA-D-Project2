from django.db import models

class Shipping(models.Model):
    order_id = models.IntegerField(unique=True)
    address = models.TextField()
    tracking_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Shipping for Order {self.order_id}"
