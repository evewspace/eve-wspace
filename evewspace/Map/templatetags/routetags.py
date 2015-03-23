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
from Map.models import KSystem
from django.core.cache import cache

register = template.Library()


@register.simple_tag
def jumps(start_sys, dest_sys):
    """
    Return string with number of stargate jumps.
    """
    return "%s" % (start_sys.jumps_to(dest_sys) - 1)


@register.simple_tag
def ly(start_sys, dest_sys):
    """
    Returns a string with ly distance.
    """
    return "%s" % (round(start_sys.distance(dest_sys), 3))
