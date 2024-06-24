from django.urls import path, include
from products.views import ProductViewSet

urlpatterns = [
    path('', ProductViewSet.as_view({'get': 'list'})),
    path('category/<str:category_name>/', ProductViewSet.as_view({'get': 'list_by_category'}), name='product-list-by-category'),
    path('price/<int:price>/', ProductViewSet.as_view({'get': 'list_by_price'}), name='product-list-by-price'),
    path('add/product/', ProductViewSet.as_view({'post': 'create'}), name='create_product'),
]
