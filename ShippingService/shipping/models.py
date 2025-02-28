from django.db import models

class Shipping(models.Model):
    order_id = models.IntegerField(unique=True)
    user_id = models.IntegerField()
    shipper_id = models.IntegerField(null=True, blank=True)
    address = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("shipped", "Shipped"), ("delivered", "Delivered"), ("cancelled", "Cancelled")],
        default="pending"
    )
    tracking_number = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Shipping {self.id} - Order {self.order_id} - {self.status}"
