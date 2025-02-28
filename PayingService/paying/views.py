from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer
from .permissions import IsBuyer, IsAdmin


# API Tạo Payment
class CreatePaymentAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsBuyer]


# API Cập nhật trạng thái Payment
class UpdatePaymentStatusAPIView(RetrieveUpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    lookup_field = "order_id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsBuyer()]
        return [IsAdmin()]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_status  = request.data.get("status")

        if not status:
            return Response({"error": "Trường status là bắt buộc"}, status=status.HTTP_400_BAD_REQUEST)

        instance.status = new_status
        instance.save()

        return Response(PaymentSerializer(instance).data, status=status.HTTP_200_OK)
