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
A registry module for registering tabs in the settings page.
"""

from django.db import models
from django.template.loader import get_template
from django.template import TemplateDoesNotExist

class NavRegistry(list):
    """
    List with methods for handling template registration.
    """
    def unregister(self, template):
        self.remove(template)

    def register(self, template):
        """
        Registers a method with its name and module.
        """
        try:
            get_template(template)
        except TemplateDoesNotExist:
            raise AttributeError("Template %s does not exist!" % template)
        self.append(template)

def _autodiscover(registry):

    import copy
    from django.conf import settings
    from importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Import alert_methods from each app
        try:
            before_import_registry = copy.copy(registry)
            import_module('%s.nav_entries' % app)
        except:
            registry = before_import_registry
            if module_has_submodule(mod, 'nav_entries'):
                raise

registry = NavRegistry()

def autodiscover():
    _autodiscover(registry)

def register(name, template):
    """Proxy for register method."""
    return registry.register(template)
