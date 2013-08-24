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
from account.profile_section_registry import registry as profile_registry
from account.user_admin_section_registry import registry as user_admin_registry
from account.group_admin_section_registry import registry as group_admin_registry
register = template.Library()

def get_active_tabs(context, registry):
    user = context['user']
    active_tabs = {}
    for key, value in registry.items():
        if not value[1]:
            active_tabs[key] = value
        elif user.has_perm(value[1]):
            active_tabs[key] = value
    return active_tabs

@register.inclusion_tag('user_admin_entries.html', takes_context=True)
def user_admin_entries(context):
    context['user_admin_registry'] = get_active_tabs(context,
            user_admin_registry)
    return context

@register.inclusion_tag('user_admin_panels.html', takes_context=True)
def user_admin_panels(context):
    context['user_admin_registry'] = get_active_tabs(context,
            user_admin_registry)
    return context

@register.inclusion_tag('group_admin_entries.html', takes_context=True)
def group_admin_entries(context):
    context['group_admin_registry'] = get_active_tabs(context,
            group_admin_registry)
    return context

@register.inclusion_tag('group_admin_panels.html', takes_context=True)
def group_admin_panels(context):
    context['group_admin_registry'] = get_active_tabs(context,
            group_admin_registry)
    return context

@register.inclusion_tag('profile_settings.html', takes_context=True)
def profile_sections(context):
    context['profile_registry'] = get_active_tabs(context, profile_registry)
    return context

@register.filter
def group_visible(groups, visible=True):
    return groups.filter(profile__visible=visible).all()
