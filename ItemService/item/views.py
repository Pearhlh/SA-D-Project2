from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import RetrieveAPIView
from .models import Category, Item
from .serializers import CategorySerializer, ItemSerializer
from .permissions import IsAdmin,IsBuyer,IsSeller


# API cho Category
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]  # Thêm kiểm tra JWT

class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "id"
    permission_classes = [IsAdmin]  # Thêm kiểm tra JWT

class ItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    parser_classes = (MultiPartParser, FormParser)  # Hỗ trợ upload file
    permission_classes = [IsSeller]

    def get_queryset(self):
        user = self.request.user
        if user.get("role") == "admin":
            return Item.objects.all()
        return Item.objects.filter(owner_id=user["id"])

class ItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = "id"
    permission_classes = [IsSeller]


