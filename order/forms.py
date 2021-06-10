from django.db.models import fields
from django.forms import ModelForm
from .forms import *
from .models import *


class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name',
                  'address', 'phone', 'city']


class UpdateStatusShippingForm (ModelForm):
    
    class Meta:
        model = Order
        fields = ['status']
