# encoding: utf-8
__author__ = 'grupo'

from django import template

register = template.Library()

@register.filter(name='field_type')
def field_type(field):
    field_name = field.field.__class__.__name__
    widget = field.field.widget.__class__.__name__
    return widget