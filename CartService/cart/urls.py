from django.urls import path
from .views import CartDetailView, CartView

urlpatterns = [
    path('carts/', CartView.as_view(), name='cart'),  # Xử lý POST
    path('carts/<int:pk>/', CartView.as_view(), name='cart-detail'),  # Xử lý PATCH, DELETE
    path('carts/user/<int:user_id>/', CartDetailView.as_view(), name='cart-user'),  # Xem giỏ hàng theo user
]
