from django.urls import include, path
from .views import *
urlpatterns = [
    path('add_to_shopcart/<int:id>', add_to_shopcart, name='add_to_shopcart'),
    path('shopcart', shopcart, name='shopcart'),
    path('delete_from_cart/<int:id>', delete_from_cart, name='delete_from_cart'),
    path('order_product/', order_product, name='order_product'),
    path('orders/', user_orders, name='user_orders'),
    path('orders_product/', user_order_product, name='user_order_product'),
    path('orderdetail/<int:id>', user_orderdetail, name='user_orderdetail'),
    path('order_product_detail/<int:id>/<int:oid>',
         user_order_product_detail, name='user_order_product_detail'),
    path('admin/orders/', get_order_admin, name='orders_admin'),
    path('admin/orders_admin_detail/<int:id>/<int:oid>',
         order_admin_detail, name='orders_admin_detail'),
    path('admin/update_shipping/<int:oid>',
         update_shipping, name='update_shipping'),
]
