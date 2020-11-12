from django import template
from myapp.models import Notification

register = template.Library()


@register.inclusion_tag('myapp/base.html')
def any_function():
    variable = Notification.objects.all().count()
    return {'msg': variable}
