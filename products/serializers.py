from rest_framework import serializers
from products.models import ProductCategory, Product, ProductImage

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'name', 'description', 'created_by', 'modified_by')
        # read_only_fields = ('id', 'name', 'description')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'user', 'category', 'name', 'description', 'initial_price', 'auction_date_time', 'status', 'bid_id', 'created_by', 'modified_by')
        # read_only_fields = ('id', 'user', 'category', 'name', 'description', 'initial_price', 'auction_date_time', 'status', 'bid_id')

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'product', 'image_url', 'created_by', 'modified_by')
        # read_only_fields = ('id', 'product', 'image_url')

