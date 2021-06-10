
from django.forms.forms import Form
from django.views.generic import ListView
from django.shortcuts import render, redirect
from .forms import *
# Create your views here.

# @login_required(login_url='login')


def add_category(request):
    forms = CreateCategoryChildForm()
    if request.method == 'POST':
        forms = CreateCategoryChildForm(request.POST, request.FILES)

        if forms.is_valid:

            try:
                category_id = request.POST['category_parent_id']
                title = request.POST['title']
                description = request.POST['description']
                image = request.FILES['image']
                category = CategoryChild(title=title, description=description,
                                          image=image, category_parent_id=category_id)
                category.save()

                return redirect('category_list')

            except Exception as e:
                print(e)
                pass
    return render(request, 'category/add_category.html', {
        'form': forms
    })


class category_list(ListView):
    model = CategoryChild
    template_name = 'category/category_list.html'
    context_object_name = 'category_list'

    def get_queryset(self):  # new
        print(self.request.GET)
        query = self.request.GET.get('q')
        if(query == None):
            object_list = CategoryChild.objects.all().filter(category_parent_id=1)
            return object_list
        object_list = CategoryChild.objects.all().filter(category_parent_id=query)
        return object_list

    def get_context_data(self, **kwargs):
        context = super(category_list, self).get_context_data(**kwargs)
        context.update({
            'category_list': CategoryParent.objects.order_by('title'),
            'more_context': CategoryParent.objects.all(),
        })
        return context


def remove_category(request, id):
    category_list = CategoryChild.objects.get(id=id)
    category_list.delete()
    return redirect('category_list')
