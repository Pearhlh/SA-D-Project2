from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterUser, LoginUser, CustomerListCreateAPIView, CustomerDetailAPIView,VerifyTokenView

urlpatterns = [
    path('auth/register/', RegisterUser.as_view(), name='register'),
    path('auth/login/', LoginUser.as_view(), name='login'),
    path("auth/verify-token/",VerifyTokenView.as_view(),name='verify-token'),
    path('customers/', CustomerListCreateAPIView.as_view(), name='customer-list'),
    path('customers/<int:pk>/', CustomerDetailAPIView.as_view(), name='customer-detail'),

    # JWT URLs
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Lấy access & refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh access token

]
