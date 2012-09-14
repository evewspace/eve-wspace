from django import template
from core.models import *

register = template.Library()

@register.simple_tag()
def typename(typeid):
    try:
        return Type.objects.get(id=typeid).name
    except Type.DoesNotExist:
        return ''
    except Type.MultipleObjectsReturned:
        return ''
