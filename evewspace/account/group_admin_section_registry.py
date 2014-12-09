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
"""
A registry module for registering sections in the group admin dialog.
"""

from django.db import models
from django.template.loader import get_template
from django.template import TemplateDoesNotExist

class GroupAdminSectionRegistry(dict):
    """
    Dict with methods for handling template registration.
    """
    def unregister(self, name):
        method = self[name]
        del self[name]

    def register(self, name, template, permission):
        """
        Registers a method with its name and module.
        """
        try:
            get_template(template)
        except TemplateDoesNotExist:
            raise AttributeError("Template %s does not exist!" % template)
        self[name] = (template, permission)

def _autodiscover(registry):

    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Import alert_methods from each app
        try:
            before_import_registry = copy.copy(registry)
            import_module('%s.group_admin_sections' % app)
        except:
            registry = before_import_registry
            if module_has_submodule(mod, 'group_admin_sections'):
                raise

registry = GroupAdminSectionRegistry()

def autodiscover():
    _autodiscover(registry)

def register(name, template, permission):
    """Proxy for register method."""
    return registry.register(name, template, permission)
