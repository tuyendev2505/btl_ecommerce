from django.urls import include, path
from .views import add_user, login_page, logout_admin, user_list, remove_user, update_user, save_update
urlpatterns = [
    path('login/', login_page, name='login'),
    path('logout/', logout_admin, name='logout_admin'),
    path('add_user/', add_user, name='add_user'),
    path('user_list/', user_list.as_view(), name='user_list'),
    path('remove_user/<int:id>', remove_user, name="remove_user"),
    path('update_user/<int:id>', update_user, name="update_user"),
    path('save_update/<int:id>', save_update, name="save_update"),
]
