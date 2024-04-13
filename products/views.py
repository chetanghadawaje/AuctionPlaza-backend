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
    http_method_names = ("get", "post")
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
        product_data = []
        for product in product_serializer.data:
            images_list = list(ProductImage.objects.filter(product=product.get('id')).values_list('id', flat=True))
            product_data.append({
                'product': product,
                'images': images_list
            })
            
        response_data = {
            "category": category_serializer.data, 
            "products": product_data
        }
        return Response({"Data": response_data, 'Status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

    def list_by_price(self, request, price=None):
        products = self.queryset.filter(initial_price=price)
        serializer = self.get_serializer(products, many=True)        
        categories = set(product.category for product in products)
        category_serializer = ProductCategorySerializer(categories, many=True)
        response_data = {
            "categories": category_serializer.data,
            "products": serializer.data
        }
        return Response({"Data": response_data, 'Status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

    def get_user_id_from_session(self, request):
        """
        Get user id from session.
        """
        return request.session.get('user_id', None)

    def create_product(self, request, category, product_data):
        """
        Create a new product.
        """
        product_data['user'] = self.get_user_id_from_session(request)
        product_data['category'] = category.id
        product_data['created_by'] = product_data['modified_by'] = self.get_user_id_from_session(request)
        product_serializer = ProductSerializer(data=product_data)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        return product_serializer

    def create_product_images(self, request, product_id, image_list):
        """
        Create images for a product.
        """
        user_id = self.get_user_id_from_session(request)
        for image in image_list:
            image_object = {
                'product': product_id,
                'image_url': image,
                'created_by': user_id,
                'modified_by': user_id
            }
            image_serializer = ProductImageSerializer(data=image_object)
            image_serializer.is_valid(raise_exception=True)
            image_serializer.save()

    def create(self, request):
        try:
            category_name = request.data.get('category')
            if category_name is None:
                return Response({"error": "Category name is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                category = ProductCategory.objects.get(name=category_name)
            except ProductCategory.DoesNotExist:
                return Response({"error": f"Category '{category_name}' does not exist"}, status=status.HTTP_404_NOT_FOUND)

            product_data = request.data
            image_list = product_data.pop('images', [])

            product_serializer = self.create_product(request, category, product_data)
            self.create_product_images(request, product_serializer.data.get('id'), image_list)

            return Response({"Data": product_serializer.data, 'Status': status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
