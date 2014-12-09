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
