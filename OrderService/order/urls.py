from django.urls import path
from .views import CreateOrderAPIView, ListOrdersAPIView, OrderDetailAPIView, CancelOrderAPIView

urlpatterns = [
    path("orders/", ListOrdersAPIView.as_view(), name="list-orders"),  # Lấy danh sách đơn hàng
    path("orders/create/", CreateOrderAPIView.as_view(), name="create-order"),  # Tạo đơn hàng (Checkout)
    path("orders/<int:pk>/", OrderDetailAPIView.as_view(), name="order-detail"),  # Xem chi tiết đơn hàng
    path("orders/<int:pk>/cancel/", CancelOrderAPIView.as_view(), name="cancel-order"),  # Hủy đơn hàng
]
