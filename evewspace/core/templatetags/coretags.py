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
from core.admin_page_registry import registry as admin_registry
from account.profile_section_registry import registry as profile_registry

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

def get_active_tabs(context, registry):
    user = context['user']
    active_tabs = {}
    for key, value in registry.items():
        if not value[1]:
            active_tabs[key] = value
        elif user.has_perm(value[1]):
            active_tabs[key] = value
    return active_tabs

@register.inclusion_tag('admin_entries.html', takes_context=True)
def admin_entries(context):
    context['admin_registry'] = get_active_tabs(context, admin_registry)
    return context

@register.inclusion_tag('admin_panels.html', takes_context=True)
def admin_panels(context):
    context['admin_registry'] = get_active_tabs(context, admin_registry)
    return context

@register.inclusion_tag('profile_settings.html', takes_context=True)
def profile_sections(context):
    context['profile_registry'] = get_active_tabs(context, profile_registry)
    return context

