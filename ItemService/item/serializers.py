import cloudinary.uploader  # Import Cloudinary
from rest_framework import serializers
from .models import Category, Item

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    image = serializers.ImageField(write_only=True, required=False)
    owner_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'category', 'name', 'description', 'price', 'stock', 'image_url', 'image', 'owner_id']
        extra_kwargs = {'image': {'write_only': True}}

    def create(self, validated_data):
        request = self.context['request']
        validated_data['owner_id'] = int(request.user["id"])

        category_id = validated_data.pop('category')
        category = Category.objects.filter(id=category_id).first()
        if not category:
            raise serializers.ValidationError("Category does not exist.")

        validated_data['category'] = category

        image = validated_data.pop('image', None)
        if image:
            upload_result = cloudinary.uploader.upload(image)
            validated_data['image_url'] = upload_result['secure_url']

        return Item.objects.create(**validated_data)
