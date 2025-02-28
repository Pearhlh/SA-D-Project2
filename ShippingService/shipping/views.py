from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from .models import Shipping
from .permissions import IsBuyer, IsShipper,IsAdminOrBuyer
from .serializers import ShippingSerializer

class RetrieveShippingAPIView(RetrieveAPIView):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    permission_classes = [IsAdminOrBuyer]

# API Tạo Shipping
class CreateShippingAPIView(CreateAPIView):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    permission_classes = [IsBuyer]

class UpdateShippingStatusAPIView(RetrieveUpdateAPIView):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    lookup_field = "order_id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAdminOrBuyer()]
        return [IsShipper()]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_status  = request.data.get("status")
        shipper_id = request.user.get("id")
        if not new_status and shipper_id:
            return Response({"error": "Trường status là bắt buộc"}, status=status.HTTP_400_BAD_REQUEST)

        instance.status = new_status
        instance.shipper_id = shipper_id
        instance.save()

        return Response(ShippingSerializer(instance).data, status=status.HTTP_200_OK)


