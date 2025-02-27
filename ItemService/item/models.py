from djongo import models
import cloudinary.uploader

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)  # Lưu URL ảnh từ Cloudinary
    owner_id = models.IntegerField()  # Lưu ID user trong MySQL
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.image_url:
            # Lấy public_id từ URL của Cloudinary để xóa
            public_id = self.image_url.split("/")[-1].split(".")[0]
            cloudinary.uploader.destroy(public_id)
        super().delete(*args, **kwargs)
