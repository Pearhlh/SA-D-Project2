from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart, CartItem
from .permissions import IsBuyer
from .serializers import CartSerializer, CartItemSerializer


class CartDetailView(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = 'user_id'
    permission_classes = [IsBuyer]

    def get_object(self):
        user_id = self.kwargs['user_id']
        cart, _ = Cart.objects.get_or_create(user_id=user_id)
        return cart



class CartView(APIView):
    permission_classes = [IsBuyer]

    def get(self, request, *args, **kwargs):
        print(request.user)
        if not request.user.get('role') == 'admin':
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user_id = request.user.get('id')  # Lấy user ID từ token thay vì request body
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity', 1)
        price = request.data.get('price')

        if not all([user_id, item_id, price]):
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        cart, _ = Cart.objects.get_or_create(user_id=user_id)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, item_id=item_id,
            defaults={"quantity": quantity, "price": price}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk=None, *args, **kwargs):
        if not pk:
            return Response({"error": "Cart item ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_item = CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)  # `partial=True` cho PATCH
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        if not pk:
            return Response({"error": "Cart item ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_item = CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response({"message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)
