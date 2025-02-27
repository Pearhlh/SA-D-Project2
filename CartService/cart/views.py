from rest_framework import generics
from .models import Cart
from .serializers import CartSerializer

class CartListCreateAPIView(generics.ListCreateAPIView):
    queryset = Cart.objects.all().order_by('-created_at')
    serializer_class = CartSerializer

class CartDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
