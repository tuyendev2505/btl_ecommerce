from django import template
from order.models import ShopCart
from category.models import CategoryChild

register = template.Library()


@register.simple_tag
def categorylist():
    return CategoryParent.objects.all()


@register.simple_tag
def shopcartcount(userid):
    count = ShopCart.objects.filter(user_id=userid).count()
    return count


@register.filter
def reset(value):
    try:
        if value == None or value == 'None':
            return 0
    except:
        pass
    return ''
