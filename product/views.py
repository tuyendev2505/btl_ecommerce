from .forms import *
from django.shortcuts import render, redirect
from .models import Product
from django.views.generic import ListView
from category.models import CategoryChild

# Create your views here.


def add_product(request):
    forms = CreateProductForm()
    if request.method == 'POST':
        forms = CreateProductForm(request.POST)

        if forms.is_valid:

            try:
                category_id = request.POST['category_child_id']
                title = request.POST['title']
                keywords = request.POST['keywords']
                description = request.POST['description']
                variant = request.POST['variant']
                name_supplier = request.POST['name_supplier']
                phone_supplier = request.POST['phone_supplier']
                product = Product(title=title, keywords=keywords, description=description, variant=variant,
                                  name_supplier=name_supplier, phone_supplier=phone_supplier, category_id=category_id)
                product.save()
                return redirect('product_list')

            except Exception as e:
                print(e)
                pass
    return render(request, 'product/add_product.html', {
        'form': forms
    })


class product_list(ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'category_list'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        if(query == None):
            object_list = Product.objects.all().filter(
                category_id=1)

            return object_list

        object_list = Product.objects.all().filter(category_id=query)
        return object_list

    def get_context_data(self, **kwargs):
        context = super(product_list, self).get_context_data(**kwargs)
        context.update({
            'category_list': CategoryChild.objects.order_by('title'),
            'more_context': CategoryChild.objects.all(),
        })
        return context


def remove_product(request, id):
    product_list = Product.objects.get(id=id)
    product_list.delete()
    return redirect('product_list')
