from django.urls import include, path
from .views import *
urlpatterns = [
    path('import_stock/', import_stock, name='import_stock'),
    path('product_in_stock/', product_in_stock, name='product_in_stock'),
    path('product_sale/<int:id>', product_sale, name='product_sale'),
    path('product_save_to_sale/', product_save_to_sale, name='product_save_to_sale'),
    path('product_sale_list/', product_sale_list, name='product_sale_list'),
    path('update_product_sale/<int:id>', update_product_sale, name='update_product_sale'),
    path('save_update_product/', save_update_product, name='save_update_product'),
    path('delete_product/<int:id>', delete_product, name='delete_product'),
    path('statistic_inventory', statistic_inventory, name='statistic_inventory'),
    path('statistic_income', statistic_income, name='statistic_income')
]
