from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
    status = serializers.ChoiceField(choices=["pending", "shipped", "delivered", "cancelled"])
