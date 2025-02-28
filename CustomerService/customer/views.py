from django.contrib.auth import authenticate, login
from django.contrib.auth.models import update_last_login
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Customer
from .permissions import IsAdminOrOwner
from .serializers import CustomerSerializer


# Danh mục
class CustomerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated,IsAdminOrOwner]


class CustomerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated,IsAdminOrOwner]



class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])  # Hash mật khẩu
            user.save()

            # Tạo JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'message': 'User registered successfully',
                'refresh': str(refresh),
                'access': access_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'bio' : user.bio
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            update_last_login(None, user)

            # Tạo JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'message': 'Login successful',
                'refresh': str(refresh),
                'access': access_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                }
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)




class VerifyTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("Headers gửi đi:", request.headers)
        auth = JWTAuthentication()
        try:
            user, _ = auth.authenticate(request)
            if user:
                return Response({
                    "id": user.id,
                    "username": user.username,
                    "role": user.role
                }, status=200)
            return Response({"error": "Invalid token"}, status=401)
        except:
            raise AuthenticationFailed("Invalid token")
