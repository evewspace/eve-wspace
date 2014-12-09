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
from Map.models import *
register = template.Library()

@register.inclusion_tag('map_list.html')
def mapnavlist(user):
    """Return list of maps that should appear in the user's nav bar."""
    #Make a list, yay!
    maplist = []
    for map in Map.objects.all():
        if map.get_permission(user) > 0:
            maplist.append(map)
    return {'maps': maplist}
