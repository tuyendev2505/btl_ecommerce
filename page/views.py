

from django.shortcuts import render
from stock.forms import CommentForm
from stock.models import Comment

# Create your views here.
from stock.models import *
from category.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import UserProfile
from .forms import SignUpForm
from users.models import User


def index(request):

    products_latest = Item.objects.all().order_by(
        '-detail_bill_id')[:4]  # last 4 products

    products_slider = Item.objects.all().order_by('detail_bill_id')[
        :4]  # first 4 products

    # products_picked = Product.objects.all().order_by(
    #     '?')[:4]  # Random selected 4 products

    page = "home"
    categories = CategoryParent.objects.all()
    categoriesChild = CategoryChild.objects.all().order_by('-id')[:4]
    context = {
        'page': page,
        'products_slider': products_slider,
        'products_latest': products_latest,
        # 'products_picked': products_picked,
        'categories': categories,
        'category_child': categoriesChild
    }
    return render(request, 'pages/index.html', context)


def aboutus(request):
    print(request.user.id)
    categories = CategoryParent.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'pages/about.html', context)


def contactus(request):
   
    return render(request, 'pages/contactus.html')


def product_detail(request, id):
    print(id)
    category = CategoryParent.objects.all()
    product = Item.objects.get(pk=id)
    print(product)

    # images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(item_id=id, status='True')
    context = {'product': product,
               'category': category,
               #    'images': images,
               'comments': comments,
               }
    return render(request, 'pages/product_detail.html', context)


def addcomment(request, id):
    print(id)
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user
    print(url)
    if request.method == 'POST':  # check post
        form = CommentForm(request.POST)
        if form.is_valid():
            try:
                data = Comment()  # create relation with model
                data.subject = form.cleaned_data['subject']
                data.comment = form.cleaned_data['comment']
                data.rate = form.cleaned_data['rate']
                data.item_id = id
                # current_user = request.user
                data.user_id = current_user.id
                data.save()  # save data to table
                messages.success(
                    request, "Your review has ben sent. Thank you for your interest.")
                return HttpResponseRedirect(url)
            except Exception as e:
                print(e)
                pass

    return HttpResponseRedirect(url)


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

    categories = CategoryParent.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'pages/login_form.html', context)


def logout_func(request):
    logout(request)
    if 'userimage' in request.session:
        del request.session['userimage']
    return HttpResponseRedirect('/')



def signup_form(request):
    if request.method == 'POST':
        forms = SignUpForm(request.POST)
        print('aaaa')
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']

            try:
                print(password)
                if password == retype_password:
                    print(password)
                    user = User.objects.create_user(
                        username=username, password=password, email=email, name=name, address=address, role="Customer")
                if(user):
                    username = forms.cleaned_data.get('username')
                    password = forms.cleaned_data.get('password')
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    # Create data in profile table for user
                    current_user = request.user
                    data = UserProfile()
                    data.user_id = current_user.id
                    data.address = address
                    data.city = "Ha noi"

                    data.image = "images/users/user.png"
                    data.save()
                    messages.success(request, 'Your account has been created!')
                    return HttpResponseRedirect('/')
                else:
                    messages.warning(request, forms.errors)
                    return HttpResponseRedirect('/signup')
            except Exception as e:
                print("exception", e)
                pass

    forms = SignUpForm()
    categories = CategoryParent.objects.all()
    context = {
        'categories': categories,
        'form': forms,
    }
    return render(request, 'pages/signup_form.html', context)
