from django.db import models

class Cart(models.Model):
    user_id = models.IntegerField(unique=True)  # Mỗi user có một giỏ hàng duy nhất
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of User {self.user_id}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    item_id = models.IntegerField()  # Tham chiếu đến Item (ở service khác)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Lưu giá tại thời điểm thêm vào giỏ
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CartItem: Cart {self.cart.id} - Item {self.item_id} ({self.quantity})"
