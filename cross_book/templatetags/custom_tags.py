from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def split_timesince(value, delimiter=None):
    return value.split(delimiter)[0]
