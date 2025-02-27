from django.db import models

class Cart(models.Model):
    user_id = models.IntegerField()
    item_id = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart: User {self.user_id} - Item {self.item_id} ({self.quantity})"
