from django import template

register = template.Library()

@register.filter
def get_at_index(list, index):
    print(list)
    return list[index-1]
