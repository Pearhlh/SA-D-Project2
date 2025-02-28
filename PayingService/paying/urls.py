from django.urls import path
from .views import CreatePaymentAPIView, UpdatePaymentStatusAPIView

urlpatterns = [
    path("payments/", CreatePaymentAPIView.as_view(), name="create-payment"),
    path("payments/<int:order_id>/", UpdatePaymentStatusAPIView.as_view(), name="update-payment-status"),
]
