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
