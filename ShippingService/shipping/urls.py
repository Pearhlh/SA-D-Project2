from django.urls import path
from .views import CreateShippingAPIView, UpdateShippingStatusAPIView

urlpatterns = [
    path("shipping/", CreateShippingAPIView.as_view(), name="create-shipping"),
    path("shipping/<int:order_id>/", UpdateShippingStatusAPIView.as_view(), name="update-shipping-status"),
]
