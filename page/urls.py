from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.aboutus, name='aboutus'),
    path('contact/', views.contactus, name='contactus'),
    path('product_detail/<int:id>',
         views.product_detail, name='product_detail'),
    path('add_comment/<int:id>',
         views.addcomment, name='add_comment'),
    path('login/', views.login_form, name='login'),
    path('logout/', views.logout_func, name='logout'),
    path('signup/', views.signup_form, name='signup'),
]
