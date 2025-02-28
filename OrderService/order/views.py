import requests
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Order, OrderItem
from .permissions import IsBuyer, IsAdminOrBuyer
from .serializers import OrderDetailSerializer
from .serializers import OrderSerializer


class CreateOrderAPIView(generics.CreateAPIView):
    permission_classes = [IsBuyer]
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.user.get("id")
        cart_item_ids = request.data.get("cart_item_ids", [])
        auth_header = {"Authorization": f"Bearer {request.auth}"}

        if not cart_item_ids:
            return Response({"error": "Vui lòng chọn ít nhất một sản phẩm để đặt hàng."}, status=status.HTTP_400_BAD_REQUEST)

        cart_response = requests.get(f"http://host.docker.internal:8001/api/carts/user/{user_id}/", headers=auth_header)
        if cart_response.status_code != 200:
            return Response({"error": "Không thể lấy giỏ hàng"}, status=status.HTTP_400_BAD_REQUEST)

        cart_data = cart_response.json()
        selected_items = [item for item in cart_data["items"] if item["id"] in cart_item_ids]

        if not selected_items:
            return Response({"error": "Không tìm thấy sản phẩm đã chọn trong giỏ hàng."}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(float(item["price"]) * item["quantity"] for item in selected_items)

        order = Order.objects.create(user_id=user_id, total_price=total_price)

        for item in selected_items:
            OrderItem.objects.create(order=order, item_id=item["item_id"], quantity=item["quantity"], price=float(item["price"]))

        for cart_item_id in cart_item_ids:
            requests.delete(f"http://host.docker.internal:8001/api/carts/{cart_item_id}/", headers=auth_header)

        # ✅ Gọi API tạo Payment
        payment_response = requests.post("http://host.docker.internal:8003/api/payments/", json={
            "order_id": order.id, "user_id": user_id, "amount": total_price
        }, headers=auth_header)

        # ✅ Gọi API tạo Shipping
        shipping_response = requests.post("http://host.docker.internal:8004/api/shipping/", json={
            "order_id": order.id, "user_id": user_id, "address": request.data.get("address", ""),  "tracking_number": None
        }, headers=auth_header)
        print(shipping_response.status_code)  # Kiểm tra mã lỗi
        print(shipping_response.json())
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class ListOrdersAPIView(generics.ListAPIView):
    permission_classes = [IsAdminOrBuyer]
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.get('role') == 'admin':
            return Order.objects.all()
        return Order.objects.filter(user_id=self.request.user.get('id')).order_by("-created_at")


class OrderDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAdminOrBuyer]
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        if self.request.user.get('role') == 'admin':
            return Order.objects.all()
        return Order.objects.filter(user_id=self.request.user.get('id'))


class CancelOrderAPIView(generics.UpdateAPIView):
    permission_classes = [IsBuyer]
    serializer_class = OrderSerializer

    def update(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs["pk"], user_id=request.user.get('id'))

        if order.status != "pending":
            return Response({"error": "Không thể hủy đơn hàng đã xử lý"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = "cancelled"
        order.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

