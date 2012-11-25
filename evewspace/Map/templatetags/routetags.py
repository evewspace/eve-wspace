from django import template
from Map.models import KSystem
from django.core.cache import cache

register=template.Library()

@register.simple_tag
def jumps(startSys, destSys):
    """
    Return string with number of stargate jumps.
    """
    return "%s" % (startSys.jumps_to(destSys) - 1)

@register.simple_tag
def ly(startSys, destSys):
    """
    Returns a string with ly distance.
    """
    return "%s" % (round(startSys.distance(destSys), 3))
