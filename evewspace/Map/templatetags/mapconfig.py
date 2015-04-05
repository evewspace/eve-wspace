#   Eve W-Space
#   Copyright 2014 Andrew Austin and contributors
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from django import template
from Map.models import Map, Destination, SignatureType, SiteSpawn, MapPermission
from django.contrib.auth.models import Group

register = template.Library()


@register.inclusion_tag('map_settings.html')
def map_global_admin():
    """
    Returns the Map admin panel for the settings page.
    """
    return {'maps': Map.objects.all(),
            'destinations': Destination.objects.all(),
            'sigtypes': SignatureType.objects.all(),
            'spawns': SiteSpawn.objects.all()}


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
        groups.append((group, perm))
    return {'map': subject, 'groups': groups}
