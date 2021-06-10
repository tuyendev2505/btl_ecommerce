from django import forms
from .models import *
from product.models import Product


class CreateImportStockForm (forms.ModelForm):

    # product_id = forms.ModelChoiceField(Product.objects.all(
    # ), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = DetailBill
        fields = "__all__"
        widgets = {
            'bill_code': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'bill_code',
                'data-val': 'true',
                'data-val-required': 'Please enter bill code',
            }),
            'price': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'price',
                'data-val': 'true',
                'data-val-required': 'Please enter Gía',
            }),
            'amount': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'amount',
                'data-val': 'true',
                'data-val-required': 'Please enter số lượng',
            }),
            'unit': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'unit',
                'data-val': 'true',
                'data-val-required': 'Please enter đơn vị',
            }),
        }


class CreateItemForm (forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control col-4',
                'id': 'title',
                'data-val': 'true',
                'data-val-required': 'Please enter tên mặt hàng',
            }),
            'price_sale': forms.TextInput(attrs={
                'class': 'form-control col-4',
                'id': 'price_sale',
                'data-val': 'true',
                'data-val-required': 'Please enter price sale',
            }),
            'amount_sale': forms.TextInput(attrs={
                'class': 'form-control col-4',
                'id': 'amount_sale',
                'data-val': 'true',
                'data-val-required': 'Please enter số lượng',
            }),
            'keywords': forms.TextInput(attrs={
                'class': 'form-control col-4',
                'id': 'keywords',
                'data-val': 'true',
                'data-val-required': 'Please enter từ khoá',
            }),

        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']
