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
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
from core.models import ConfigEntry

class Command(BaseCommand):
    """
    Load default settings from each application's default_settings.py file.
    """
    def handle(self, *args, **options):
        if not args:
            for app in settings.INSTALLED_APPS:
                mod = import_module(app)
                if module_has_submodule(mod, "default_settings"):
                    try:
                        def_mod = import_module("%s.default_settings" % app)
                        def_mod.load_defaults()
                    except:
                        raise
        else:
            for app in args:
                try:
                    mod = import_module(app)
                except ImportError:
                    raise CommandError('App %s could not be imported.' % app)
                if module_has_submodule(mod, "default_settings"):
                    try:
                        def_mod = import_module("%s.default_settings" % app)
                        def_mod.load_defaults()
                    except:
                        raise
