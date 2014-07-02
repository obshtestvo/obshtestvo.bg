import json

from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django import template

register = template.Library()


@register.filter(name='jsonify')
def jsonify(object):
    if isinstance(object, QuerySet):
        return serialize('json', object)
    return json.dumps(object)

@register.simple_tag(takes_context=True)
def query(context, **kwargs):
    request = context.get('request')
    params = request.params.copy()

    for name, value in kwargs.iteritems():
        if params.get(name, None) is not None and value is None:
            del params[name]
        if value is not None:
            params[name] = value

    query_string = params.urlencode()

    return '' if not query_string else '?'+query_string