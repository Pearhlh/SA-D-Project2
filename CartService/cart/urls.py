from django.urls import path
from .views import CartListCreateAPIView, CartDetailAPIView

urlpatterns = [
    path('carts/', CartListCreateAPIView.as_view(), name='cart-list-create'),  # Lấy danh sách & thêm mới
    path('carts/<int:pk>/', CartDetailAPIView.as_view(), name='cart-detail'),  # Xem, sửa, xóa sản phẩm trong giỏ
]
