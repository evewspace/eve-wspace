from django import template
from POS.models import POS

register=template.Library()


@register.inclusion_tag('poslist.html')
def poslist(system):
    poses = POS.objects.filter(system=system)
    return {'poses': poses, 'system': system}


@register.inclusion_tag('posdetails_small.html')
def posdetails(system, pos):
    return {'pos' : pos, 'system': system}
