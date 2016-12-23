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
from core.templatetags.coretags import registry_tag, registry_names_tag
from core.utils import get_config 
register = template.Library()

registry_names_tag(register, 'user_admin_entries', 'user_admin_sections')

registry_tag(register, 'user_admin_panels', 'user_admin_sections')

registry_names_tag(register, 'group_admin_entries', 'group_admin_sections')

registry_tag(register, 'group_admin_panels', 'group_admin_sections')

registry_tag(register, 'profile_settings', 'profile_pages')

@register.filter
def group_visible(groups, visible=True):
    return groups.filter(profile__visible=visible).all()

@register.assignment_tag()
def sso_enabled():
    return get_config("SSO_LOGIN_ENABLED", None).value
    
