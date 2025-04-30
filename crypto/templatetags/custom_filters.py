from django import template

register = template.Library()

@register.filter
def format_coin(value):
    return value.upper().replace('_', '/')
