from django.urls import include, path
from .views import add_category, category_list, remove_category
urlpatterns = [

    path('add_category/', add_category, name='add_category'),
    path('category_list/', category_list.as_view(), name='category_list'),
    path('remove_category/<int:id>', remove_category, name="remove_category"),

]
