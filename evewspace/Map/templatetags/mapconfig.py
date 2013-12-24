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
from Map.models import Map, Destination, SignatureType, SiteSpawn, MapPermission
from django.contrib.auth.models import Group

register = template.Library()

@register.inclusion_tag('map_settings.html')
def map_global_admin():
    """
    Returns the Map admin panel for the settings page.
    """
    return {'maps': Map.objects.all(), 'destinations': Destination.objects.all(),
            'sigtypes': SignatureType.objects.all(),
            'spawns': SiteSpawn.objects.all(),}


@register.inclusion_tag('map_settings_single.html')
def map_settings(subject):
    """
    Returns the config block for a sngle map's general settings.
    """
    groups = []
    for group in Group.objects.all():
        if MapPermission.objects.filter(map=subject, group=group).exists():
            perm = MapPermission.objects.get(map=subject, group=group).access
        else:
            perm = 0
        groups.append((group,perm))
    return {'map': subject, 'groups': groups}
