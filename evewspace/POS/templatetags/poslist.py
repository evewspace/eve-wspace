from django import template
import POS

register=template.Library()

@register.inclusion_tag('poslist.html')
def poslist(system):
	poses = POS.objects.filter(location__system=system)
	return {'poses': poses}

@register.inclusion_tag('posdetails_small.html')
def posdetails(pos):
	return {'pos' : pos}
