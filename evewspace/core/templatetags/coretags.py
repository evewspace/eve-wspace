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
from core.models import Type
from core.nav_registry import registry as nav_registry

register = template.Library()

@register.simple_tag()
def typename(typeid):
    try:
        return Type.objects.get(id=typeid).name
    except Type.DoesNotExist:
        return ''
    except Type.MultipleObjectsReturned:
        return ''

@register.inclusion_tag('nav_entries.html', takes_context=True)
def nav_entries(context):
    """
    Renders dynamic nav bar entries from nav_registry for the provided user.
    """
    context['nav_registry'] = nav_registry
    return context
