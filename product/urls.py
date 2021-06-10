from django.urls import include, path
from .views import add_product, product_list, remove_product
urlpatterns = [
    path('add_product/', add_product, name='add_product'),
    path('product_list/', product_list.as_view(), name='product_list'),
    path('remove_product/<int:id>', remove_product, name="remove_product"),
]
