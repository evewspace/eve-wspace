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
from core.models import Type
from core.utils import get_config
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

@register.inclusion_tag('feedback_panel.html')
def feedback_panel():
    return {'render': get_config("CORE_FEEDBACK_ENABLED",
        None).value == "1"}
