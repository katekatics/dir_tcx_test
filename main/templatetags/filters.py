from django import template

register = template.Library()

@register.filter
def range_len(list):
    return range(len(list))

@register.filter
def elem(list, index):
    return list[index]

@register.filter
def percent(value, arg):
    if value % arg == 0:
        return True
    else:
        return False

@register.filter
def fori(object):
    list = [i for i in object]
    return list


@register.filter
def keys(object, item=None):
    if not item:
        return list(object.keys())
    else:
        return list(object[item].keys())


@register.filter
def index(list, item):
    return list.index(item)



@register.filter() 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 

