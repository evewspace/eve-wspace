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
    from django.utils.importlib import import_module
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
