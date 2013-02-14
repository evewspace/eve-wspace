#    Eve W-Space
#    Copyright (C) 2013  Andrew Austin and other contributors
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version. An additional term under section
#    7 of the GPL is included in the LICENSE file.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
from django import template
from Map.models import *
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
    elif not user.is_anonymous():
        #User is in a restricted group, only add maps with access > 0
        for map in Map.objects.all():
            if map.get_permission(user) > 0:
                maplist.append(map)
    return {'maps': maplist}
