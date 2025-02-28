from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'username', 'email','bio', 'role', 'password')
        extra_kwargs = {'password': {'write_only': True}}
