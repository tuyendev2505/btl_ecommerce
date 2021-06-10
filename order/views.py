from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from stock.models import Item
from .models import *
from .forms import *
from category.models import *
from django.db import transaction
from page.models import UserProfile
from users.models import User
from django.db import connection, transaction, connections
# Create your views here.
from django.utils.crypto import get_random_string

# Create your views here.


# @login_required(login_url='/login')  # Check login
def add_to_shopcart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    print(url)
    current_user = request.user  # Access User Session information

    checkinproduct = ShopCart.objects.filter(
        item_id=id, user_id=current_user.id)  # Check product in shopcart
    if checkinproduct:
        control = 1  # The product is in the cart
    else:
        control = 0  # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update  shopcart

                data = ShopCart.objects.get(
                    item_id=id,  user_id=current_user.id)
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else:  
                data = ShopCart()
                data.user_id = current_user.id
                data.item_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product added to Shopcart ")
        return HttpResponseRedirect(url)

    else:  # if there is no post
        if control == 1:  # Update  shopcart
            data = ShopCart.objects.get(
                item_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()
        else:  # Inser to Shopcart
            data = ShopCart()  #
            data.user_id = current_user.id
            data.item_id = id
            data.quantity = 1
            data.save()  #
        messages.success(request, "Product added to Shopcart")
        return HttpResponseRedirect(url)


def shopcart(request):
    categories = CategoryParent.objects.all()
    current_user = request.user  # 
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0

    for rs in shopcart:
        total += rs.item.price_sale * rs.quantity
    context = {'shopcart': shopcart,
               'categories': categories,
               'total': total,
               }
    return render(request, 'pages/shopcart_products.html', context)


def delete_from_cart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item deleted form Shopcart.")
    return HttpResponseRedirect("/order/shopcart")


def order_product(request):
    category = CategoryParent.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    print('shop', shopcart)
    for rs in shopcart:
        total += rs.item.price_sale * rs.quantity
    print(total)

    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)

        if form.is_valid():

            try:
                data = Order()
            # get product quantity from form
                data.first_name = form.cleaned_data['first_name']
                data.last_name = form.cleaned_data['last_name']
                data.address = form.cleaned_data['address']
                data.city = form.cleaned_data['city']
                data.phone = form.cleaned_data['phone']
                data.user_id = current_user.id
                data.total = total
                order_code = get_random_string(5).upper()  # random cod
                data.code = order_code
                data.save()

                with transaction.atomic():
                    print(data.id)
                    for rs in shopcart:

                        detail = OrderItem()
                        detail.order_id = data.id  # Order Id
                        detail.item_id = rs.item_id
                        detail.user_id = current_user.id
                        detail.quantity = rs.quantity
                        detail.price = rs.item.price_sale
                        detail.amount = rs.item.amount_sale
                        detail.save()
                        # ***Reduce quantity of sold product from Amount of Product
                        with transaction.atomic():
                            product = Item.objects.get(
                                detail_bill_id=rs.item_id)
                            product.amount_sale -= rs.quantity
                            product.save()

                    # Clear & Delete shopcart
                    ShopCart.objects.filter(user_id=current_user.id).delete()
                    request.session['cart_items'] = 0
                    messages.success(
                        request, "Your Order has been completed. Thank you ")
                    return render(request, 'pages/order_completed.html', {'ordercode': order_code, 'category': category})

            except Exception as e:
                print(e)
                pass

        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/order_product")

    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               'form': form,
               'profile': profile,
               }
    return render(request, 'pages/order_form.html', context)


def user_orders(request):
    # category = Category.objects.all()
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    categories = CategoryParent.objects.all()
    context = {  # 'category': category,
        'orders': orders,
        'category': categories,
    }
    return render(request, 'pages/user_orders.html', context)


def user_orderdetail(request, id):
    category = CategoryParent.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderItem.objects.filter(order_id=id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'pages/user_order_detail.html', context)


def user_order_product(request):
    category = CategoryParent.objects.all()
    current_user = request.user
    order_product = OrderItem.objects.filter(
        user_id=current_user.id).order_by('-id')
    context = {
        'category': category,
        'order_product': order_product,
    }
    return render(request, 'pages/user_order_products.html', context)


def user_order_product_detail(request, id, oid):
    category = CategoryParent.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderItem.objects.filter(id=id, user_id=current_user.id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'pages/user_order_detail.html', context)


# get order admin

def get_order_admin(request):
    orderitems = OrderItem.objects.select_related(
        'order').select_related('item').select_related('user')
    return render(request, 'order/order_list.html', {
        'order_items': orderitems
    })


def order_admin_detail(request, id, oid):
    orderitem = OrderItem.objects.select_related(
        'order').select_related('item').get(id=id)
    listOrderItem = OrderItem.objects.filter(order_id=oid)
    sum = 0
    for i in listOrderItem:
        sum += i.price * i.quantity
    forms = UpdateStatusShippingForm()
    return render(request, 'order/detail_order.html', {
        'order_item': orderitem,
        'form': forms,
        'orderitems': listOrderItem,
        'sum': sum
    })


def update_shipping(request, oid):

    order = Order.objects.get(id=oid)
    status = order.status
    cursor = connections['default'].cursor()
    if status == 'New':
        Order.objects.filter(id=oid).update(status="Shipped")
    else:
         Order.objects.filter(id=oid).update(status="New")
    return redirect('orders_admin')
