from django.contrib import admin
from products.models import ProductCategory, Product, ProductImage

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name', 'description')

admin.site.register(ProductCategory, ProductCategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'name', 'description', 'initial_price', 'auction_date_time', 'status', 'bid_id')
    list_filter = ('user', 'category', 'name', 'description', 'initial_price', 'auction_date_time', 'status', 'bid_id')

admin.site.register(Product, ProductAdmin)

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_url')
    list_filter = ('product', 'image_url')

admin.site.register(ProductImage, ProductImageAdmin)
