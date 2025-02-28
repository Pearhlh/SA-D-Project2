from rest_framework import serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'item_id', 'quantity', 'price', 'created_at', 'updated_at']
        read_only_fields = ['cart', 'created_at', 'updated_at']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user_id', 'items', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
