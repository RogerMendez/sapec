from django import template

register = template.Library()
import datetime

@register.filter(name='cut')
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value + arg

@register.filter(name='restar')
def restar(hora1, hora2):
    #hora1 - hora2
    h1 = int(hora1[0:2])
    h2 = int(hora2[0:2])
    m1 = int(hora1[3:5])
    m2 = int(hora2[3:5])
    h = h1 - h2
    m  = m1 - m2
    if m < 0:
        m = m + 60
        h -= 1
    if m < 10:
        min = "0" + str(m)
    else:
        min = str(m)
    if h < 10 :
        hr = "0" + str(h)
    else:
        hr = str(h)
    return str(hr) + ":" + str(min)