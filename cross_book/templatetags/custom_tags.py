from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def split_timesince(value, delimiter=None):
    return value.split(delimiter)[0]


@register.filter(is_sage=True)
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)
