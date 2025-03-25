from django import template

register = template.Library()


@register.filter(name='should_show_home_link')
def should_show_home_link(request):
    paths = ('/ordering', '/total_price', '/search')
    return any(path in request.path for path in paths)