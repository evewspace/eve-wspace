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
from core.registry import Registry
from core.models import Type
from core.utils import get_config
register = template.Library()

@register.simple_tag()
def typename(typeid):
    try:
        return Type.objects.get(id=typeid).name
    except (Type.DoesNotExist, Type.MultipleObjectsReturned):
        return ''

def registry_tag(register, name, registry_name):
    def tag(context):
        registry = Registry.get_registry(registry_name)
        context[name] = registry.get_visible(context['user'])
        return context
    wrapper = register.inclusion_tag(name + '.html', takes_context=True, name=name)
    wrapper(tag)

def registry_names_tag(register, name, registry_name):
    def tag(context):
        registry = Registry.get_registry(registry_name)
        context[name] = (k for k,v in registry.get_visible(context['user']))
        return context
    wrapper = register.inclusion_tag(name+'.html', takes_context=True, name=name)
    wrapper(tag)

registry_tag(register, 'nav_entries', 'nav_entries')

registry_names_tag(register, 'admin_entries', 'admin_pages')

registry_tag(register, 'admin_panels', 'admin_pages')

@register.inclusion_tag('feedback_panel.html')
def feedback_panel():
    return {'render': get_config("CORE_FEEDBACK_ENABLED",
        None).value == "1"}
