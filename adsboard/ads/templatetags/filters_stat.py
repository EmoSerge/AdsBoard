from django import template


register = template.Library()


@register.filter()
def status_delete(response):
    return response.filter(status_delete=False, status_accept=False)


@register.filter()
def status_accept(response):
    return response.filter(status_accept=True)


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
