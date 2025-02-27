from rest_framework import viewsets
from .models import Shipping
from .serializers import ShippingSerializer

class ShippingViewSet(viewsets.ModelViewSet):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
