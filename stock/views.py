
from json import dumps
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from .forms import *
from category.models import *
from product.models import *
from django.core import serializers
from django.db import connection, transaction, connections
from .models import *
import datetime
# Create your views here.


def import_stock(request):
    forms = CreateImportStockForm()
    categories = CategoryChild.objects.all()
    productAll = Product.objects.all().values('id', 'title', 'category_id')

    current_user = request.user
    if request.method == 'POST':
        forms = CreateImportStockForm(request.POST)
        if(forms.is_valid):
            cursor = connections['default'].cursor()
            cursor.execute(
                "INSERT INTO stock_stock(user_id) VALUES( %s )", [current_user.id])
            try:
                with transaction.atomic():
                    product_id = request.POST['product']
                    bill_code = request.POST['bill_code']
                    price = request.POST['price']
                    amount = request.POST['amount']
                    unit = request.POST['unit']

                    detail_bill = DetailBill(
                        product_id=product_id, bill_code=bill_code, price=price, amount=amount, unit=unit)
                    detail_bill.stock_id = cursor.lastrowid
                    detail_bill.save()
                    return redirect('product_in_stock')
            except Exception as e:
                print('aaaa', e)
                pass

    return render(request, 'stock/import_stock.html', {
        'form': forms,
        'categories': categories,
        'productAll': dumps(list(productAll))
    })


def json_serial(o):
    if isinstance(o, datetime.date):
        return o.__str__()


def product_in_stock(request):

    product = []
    category_child = CategoryChild.objects.all()
    item = Item.objects.all()

    if request.method == 'GET':
        q_category = request.GET.get('q-category')
        q_search = request.GET.get('q-search')

        if q_category == None and q_search == None:
            product = DetailBill.objects.distinct().select_related('product')
        else:
            q_search = '%' + q_search + '%'
            print(q_search)

            cursor = connections['default'].cursor()
            cursor.execute(
                'Select deb.id as id, bill_code, unit, p.title as p_title,   p.category_id as cate_id, cc.title as cc_title, p.id as p_id,price, amount from detail_bill as deb ' +
                'inner join product_product as p on deb.product_id = p.id inner join category_child as cc on p.category_id = cc.id and p.category_id = %s ', [q_category])
            product_fetch = cursor.fetchall()
            product_dumps = dumps(product_fetch, default=json_serial)
            product_in_s = []
            for i in eval(product_dumps):
                dic = {}
                dic['id'] = i[0]
                dic['bill_code'] = i[1]
                dic['unit'] = i[2]
                dic['p_title'] = i[3]
                dic['cate_id'] = i[4]
                dic['cc_title'] = i[5]
                dic['p_id'] = i[6]
                dic['price'] = i[7]
                dic['amount'] = i[8]
                product_in_s.append(dic)

            return render(request, 'stock/stock_product.html', {
                'product_in_stock': product_in_s,
                'category_child': category_child,
                'item': item
            })

    return render(request, 'stock/stock_product.html', {
        'product_in_stock': product,
        'category_child': category_child,
        'item': item
    })


def product_sale(request, id):
    item = Item.objects.filter(detail_bill_id=id)
    print(item)
    if item:
        return redirect('product_in_stock')

    forms = CreateItemForm()
    cursor = connections['default'].cursor()
    cursor.execute(
        'Select deb.id as id, bill_code, unit, p.title as p_title, p.category_id as cate_id, cc.title as cc_title, p.id as p_id,price, amount from detail_bill as deb  inner join product_product as p on deb.product_id = p.id ' +
        'inner join category_child as cc on p.category_id = cc.id and deb.id = (%s)', [id])
    product_fetch = cursor.fetchall()
    product_dumps = dumps(product_fetch, default=json_serial)
    dic = {}
    for i in eval(product_dumps):
        dic['id'] = i[0]
        dic['bill_code'] = i[1]
        dic['unit'] = i[2]
        dic['p_title'] = i[3]
        dic['cate_id'] = i[4]
        dic['cc_title'] = i[5]
        dic['p_id'] = i[6]
        dic['price'] = i[7]
        dic['amount'] = i[8]

    return render(request, 'stock/product_sale.html', {
        'product_export': dic,
        'form': forms
    })


def update_product_sale(request, id):
    print(id)
    item = Item.objects.get(detail_bill_id=id)
    print(item)
    if item:
        return render(request, 'stock/update_product_sale.html', {'item': item})
    return redirect('product_sale_list')


def save_update_product(request):
    if request.method == 'POST':
        id = request.POST['id']
        title = request.POST['title']
        price_sale = request.POST['price_sale']
        amount_sale = request.POST['amount_sale']
        keywords = request.POST['keywords']
        description = request.POST['description']

        item = Item.objects.filter(detail_bill_id=id).update(title=title, price_sale=price_sale,
                                                             amount_sale=amount_sale, keywords=keywords, description=description)
        if item:
            return redirect('product_sale_list')


def delete_product(request, id):
    item = Item.objects.filter(detail_bill_id=id).delete()
    if item:
        return redirect('product_sale_list')


def product_save_to_sale(request):
    forms = CreateItemForm()
    if request.method == 'POST':
        forms = CreateItemForm(request.POST, request.FILES)
        if forms.is_valid:
            try:
                detail_bill_id = request.POST['id']
                price_sale = request.POST['price_sale']
                amount_sale = request.POST['amount_sale']
                keywords = request.POST['keywords']
                variant = request.POST['variant']
                description = request.POST['description']
                image_sale = request.FILES['image_sale']
                title = request.POST['title']
                detail_bill = DetailBill.objects.get(
                    pk=int(detail_bill_id))
                item = Item(title=title, price_sale=price_sale, description=description, amount_sale=amount_sale, keywords=keywords, variant=variant,
                            image_sale=image_sale, detail_bill=detail_bill)
                item.save()
                return redirect('product_sale_list')

            except Exception as e:
                print("exception", e)
                pass
    return render(request, 'category/add_category.html', {
        'form': forms
    })


def product_sale_list(request):

    cursor = connections['default'].cursor()
    cursor.execute(
        'Select it.detail_bill_id as id, unit, p.title as p_title, p.id as p_id,it.price_sale as price_sale, it.amount_sale as amount_sale, it.image_sale as image_sale from detail_bill as deb ' +
        'inner join item as it on it.detail_bill_id = deb.id ' +
        'inner join product_product as p on deb.product_id = p.id ')
    product_fetch = cursor.fetchall()
    product_dumps = dumps(product_fetch, default=json_serial)

    product_sale = []
    for i in eval(product_dumps):
        dic = {}
        dic['id'] = i[0]
        dic['unit'] = i[1]
        dic['p_title'] = i[2]
        dic['p_id'] = i[3]
        dic['price_sale'] = i[4]
        dic['amount_sale'] = i[5]
        url = i[6].split('/')
        print(url)
        dic['image_sale'] = i[6]
        product_sale.append(dic)

    return render(request, 'stock/product_sale_list.html', {
        'product_sale_list': product_sale,
    })


def statistic_inventory(request):
    bill = DetailBill.objects.select_related('product').all()
    total_bill = 0
    for t_b in bill:
        total_bill += t_b.price * t_b.amount

    return render(request, 'stock/statistic_bill.html', {
        'bill': bill,
        'total_bill': total_bill
    })


def statistic_income(request):
    cursor = connections['default'].cursor()
    cursor.execute('Select p.title, deb.price, deb.amount, deb.unit, it.price_sale, it.amount_sale, quantity, price_order, deb.created_at from detail_bill as deb ' +
                   'left join item as it on it.detail_bill_id = deb.id  ' +
                   'left join product_product as p on deb.product_id = p.id  ' +
                   'left join (select item_id, sum(quantity) as quantity, sum(price) as price_order from order_item group by item_id) as oi on oi.item_id = it.detail_bill_id')

    product_fetch = cursor.fetchall()

    print(product_fetch)

    return render(request, 'stock/statistic_income.html', {
        'product_income': product_fetch,
    })
