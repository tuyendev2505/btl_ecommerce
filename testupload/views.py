from django.shortcuts import render, redirect
from .forms import *
# Create your views here.

# @login_required(login_url='login')


def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = UploadForm()
    return render(request, 'category/add_category.html', {'form': form})

# Create your views here.

