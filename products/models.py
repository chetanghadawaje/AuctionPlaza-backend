import uuid
from django.db import models
from auction_plaza.utils.models_utils import BaseModel
from users.models import User


class ProductCategory(BaseModel):
    name = models.CharField(max_length=100, unique=True)  
    description = models.TextField(blank=False)  
    
    def __str__(self):
        return self.name


class Product(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_products')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='category_products')
    name = models.CharField(max_length=100)
    description = models.TextField()
    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    auction_date_time = models.DateTimeField()
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('inprocess', 'Inprocess'),
        ('completed', 'Completed'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')
    bid_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
 
    def __str__(self):
        return self.name
    
 
class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()
 
    def __str__(self):
        return f"Image for {self.product.name}"
 