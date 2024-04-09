import logging
from rest_framework.response import Response
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend

from auction_plaza.utils.validation_error_utils import get_error_message_in_serializer
from products.models import ProductCategory, Product, ProductImage
from products.serializers import ProductCategorySerializer, ProductSerializer, ProductImageSerializer
from users.auth_utils import Authenticated

logger = logging.getLogger(__name__)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    http_method_names = ("get")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'name', 'description', 'initial_price']
    permission_classes = [Authenticated]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def list_by_category(self, request, category_name=None):
        if category_name is None:
            return Response({"error": "Category name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            category = ProductCategory.objects.get(name=category_name)
        except ProductCategory.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        
        products = self.queryset.filter(category=category.id)
        product_serializer = self.get_serializer(products, many=True)
        category_serializer = ProductCategorySerializer(category)
        
        response_data = {
            "category": category_serializer.data, 
            "products": product_serializer.data
        }
        return Response(response_data)

    def list_by_price(self, request, price=None):
        products = self.queryset.filter(initial_price=price)
        serializer = self.get_serializer(products, many=True)        
        categories = set(product.category for product in products)
        category_serializer = ProductCategorySerializer(categories, many=True)
        response_data = {
            "categories": category_serializer.data,
            "products": serializer.data
        }
        return Response(response_data)
