from django import forms
from .models import *
from category.models import CategoryChild
from .models import Product

class CreateProductForm(forms.ModelForm):
    category_child_id = forms.ModelChoiceField(CategoryChild.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'title',
                'data-val': 'true',
                'data-val-required': 'Please enter title',
            }),
            'keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'keywords',
                'data-val': 'true',
                'data-val-required': 'Please enter keywords',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'description',
                'data-val': 'true',
                'data-val-required': 'Please enter description',
            }),
            'name_supplier': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'keywords',
                'data-val': 'true',
                'data-val-required': 'Please enter name',
            }),
            'phone_supplier': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'keywords',
                'data-val': 'true',
                'data-val-required': 'Please enter phone',
            }),




        }
