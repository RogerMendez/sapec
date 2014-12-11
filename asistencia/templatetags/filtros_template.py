from django import template

register = template.Library()

@register.filter(name='cut')
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value + arg

@register.filter(name='restar')
def restar(num1, num2):
    return  num1 - num2