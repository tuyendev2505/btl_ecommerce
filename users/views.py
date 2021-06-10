from django.db import models
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages


def login_page(request):
    forms = LoginForm()
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            print(password)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                current_user = request.user
                role = 0
                if current_user.role == 'Admin':
                    role = 1
                elif current_user.role == 'Staff-stock':
                    role = 2
                elif current_user.role == 'Staff-sale':
                    role = 3
                request.session['role'] = role
                return redirect('dashboard')
    context = {'form': forms}
    return render(request, 'users/login.html', context)



# @login_required(login_url='login')
def add_user(request):
    forms = CreateUser()
    if request.method == 'POST':
        forms = CreateUser(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']
            role = forms.cleaned_data['role']
            role = dict(forms.fields['role'].choices)[role]
            print(password)
            print(retype_password)
            if password == retype_password:
                user = User.objects.create_user(
                    username=username, password=password, email=email, name=name, address=address, role=role)
                if(user):
                    return redirect('user_list')

    context = {
        'form': forms
    }
    return render(request, 'users/add_user.html', context)


class user_list(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'user_list'


def remove_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('user_list')


def update_user(request, id):
    user = User.objects.get(id=id)
    return render(request, 'users/update_user.html', {'user': user})


def save_update(request, id):
    user = User.objects.get(id=id)
    form = UpdateUser(request.POST, instance=user)
    print(form)
    if form.is_valid():
        form.save()
        return redirect("user_list")
    return render(request, 'users/update_user.html', {'user': user})



def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            return HttpResponseRedirect('/')
        else:
            messages.warning(
                request, "Login Error !! Username or Password is incorrect")
            return HttpResponseRedirect('/login')

    categories = Category.objects.all()
    context = {  
        'categories': categories
    }
    return render(request, 'user/login_form.html', context)


def logout_admin(request):
    logout(request)
    if 'role' in request.session:
        del request.session['role']
    return HttpResponseRedirect('/users/login/')