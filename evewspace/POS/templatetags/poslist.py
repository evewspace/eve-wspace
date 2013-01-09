from django import template
from POS.models import POS

register=template.Library()


@register.inclusion_tag('poslist.html', takes_context=True)
def poslist(context, system):
    poses = POS.objects.filter(system=system)
    return {'poses': poses, 'system': system, 'request': context['request']}


@register.inclusion_tag('posdetails_small.html', takes_context=True)
def posdetails(context, system, pos):
    return {'pos' : pos, 'system': system, 'perms': context['perms']}
