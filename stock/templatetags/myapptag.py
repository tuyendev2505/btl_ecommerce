from django import template


register = template.Library()


@register.simple_tag
def reset(value):
    try:
        if value == None or value == 'None':
            return 0
    except:
        pass
    return value
