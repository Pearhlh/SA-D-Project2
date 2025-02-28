from rest_framework import serializers
from .models import Shipping

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = "__all__"
    status = serializers.ChoiceField(choices=["pending", "shipped", "delivered", "cancelled"])
