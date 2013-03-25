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
A registry module for registering alert methods.
"""

from django.db import models
from method_base import AlertMethodBase

class MethodRegistry(dict):
    """
    Dict with methods for handling method registration.
    """
    def unregister(self, name):
        method = self[name]
        del self[name]

    def register(self, name, module):
        """
        Registers a method with its name and module.
        """
        if not issubclass(module, AlertMethodBase):
            raise AttributeError("Module given to MethodRegistry not valid")
        if not name:
            raise AttributeError("MethodRegistry not given a name for module.")

        self[name] = module

def _autodiscover(registry):

    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodules

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Import alert_methods from each app
        try:
            before_import_registry = copy.copy(registry)
            impot_module('%s.alert_methods' % app)
        except:
            registry = before_import_registry
            if module_has_submodule(mod, 'alert_methods'):
                raise

registry = MethodRegistry()

def autodiscover():
    _autodiscover(registry)

def register(name, module):
    """Proxy for register method."""
    return registry.register(name, module)
