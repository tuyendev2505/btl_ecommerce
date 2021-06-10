from django import forms
from .models import *


class CreateCategoryChildForm(forms.ModelForm):

    category_parent_id = forms.ModelChoiceField(CategoryParent.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = CategoryChild
        fields = "__all__"
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'title',
                'data-val': 'true',
                'data-val-required': 'Please enter title',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'description',
                'data-val': 'true',
                'data-val-required': 'Please enter description',
            }),




        }
class CreateCategoryParent(forms.ModelForm):
    class Meta:
        model = CategoryParent
        fields = "__all__"
