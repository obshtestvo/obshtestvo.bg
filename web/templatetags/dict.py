from django import template

register = template.Library()

@register.filter
def key_or_attr(data, key):
    if isinstance(key, basestring) and hasattr(data, key):
        return getattr(data, key)
    if key in data:
        return data[key]
    return {}
