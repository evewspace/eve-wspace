from django import template
from Map.models import *
from Map.utils import check_map_permission
register = template.Library()

@register.inclusion_tag('map_list.html')
def mapnavlist(user):
    """Return list of maps that should appear in the user's nav bar."""
    #Make a list, yay!
    maplist = []
    #Check to see if user is unrestricted, then add all maps that do not
    #require explicit permissions
    if user.has_perm('Map.map_unrestricted'):
        if Map.objects.filter(explicitperms=False).count() != 0:
            for map in Map.objects.filter(explicitperms=False).all():
                maplist.append(map)
    else:
        #User is in a restricted group, only add maps with access > 0
        for map in Map.objects.get_all():
            if check_map_permission(user, map) > 0:
                maplist.append(map)
    return {'maps': maplist}
