from django import template
from Map.models import *

register = template.Library()

@register.inclusion_tag('map_list.html')
def mapnavlist(user):
    """Return list of maps that should appear in the user's nav bar."""
    #Make a list, yay!
    maplist = []
    #Check to see if user is unrestricted, then add all maps that do not require explicit permissions
    if user.has_perm('Map.map_unrestricted'):
        if Map.objects.filter(explicitperms = False).count() != 0:
            maplist.append(Map.objects.get(explicitperms = False))
    else:
        #User is in a restricted group, only add maps with MapPermission entry
        for map in Map.objects.all():
            for group in user.groups:
                if MapPermission.objects.filter(map=map, group=group, view=True).count() > 0:
                    maplist.append(map)
    #Add maps with explicit permissions if group is in MapPermissions
    if Map.objects.filter(explicitperms = False).count() != 0:
        for map in Map.objects.get(explicitperms = True):
            for group in user.groups:
                if MapPermission.objects.filter(map=map, group=group, view=True).count() > 0:
                    maplist.append(map)
    return {'maps': maplist}
