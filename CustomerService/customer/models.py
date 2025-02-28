from django.contrib.auth.models import AbstractUser
from django.db import models

class Customer(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
        ('shipper', 'Shipper'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    name = models.CharField(max_length=200, null=True)
    bio = models.TextField(null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} - {self.role}"