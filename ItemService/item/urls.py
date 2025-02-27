from django.urls import path
from .views import CategoryListCreateAPIView, CategoryDetailAPIView, ItemListCreateAPIView, ItemDetailAPIView

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:id>/', CategoryDetailAPIView.as_view(), name='category-detail'),

    path('items/', ItemListCreateAPIView.as_view(), name='item-list-create'),
    path('items/<int:id>/', ItemDetailAPIView.as_view(), name='item-detail'),  # Đổi từ _id thành id
]
