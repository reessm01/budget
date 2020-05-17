from django import template

register = template.Library()


@register.filter
def no_snake(s):
    return s.replace('_', ' ')
