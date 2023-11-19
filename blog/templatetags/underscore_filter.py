from django import template

# variable to register the filter
register = template.Library()

@register.filter(name='underscore')
def underscore(value):
    return value.replace(' ', '_')