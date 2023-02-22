from django import template


register = template.Library()


@register.filter()
def status_delete(response):
    return response.filter(status_delete=False, status_accept=False)


@register.filter()
def status_accept(response):
    return response.filter(status_accept=True)
