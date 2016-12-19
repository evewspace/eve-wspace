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
from core.models import ConfigEntry

def get_config(name, user):
    """
    Gets the correct config value for the given key name.
    Value with the given user has priority over any default value.
    """
    try:
        return ConfigEntry.objects.get(name=name, user=user)
    except ConfigEntry.DoesNotExist:
        return ConfigEntry.objects.get(name=name, user=None)

def load_defaults(defaults, reset=False, stdout=None):
    if stdout is None:
        from sys import stdout
    for setting in defaults:
        config, created = ConfigEntry.objects.get_or_create(name=setting[0], user=None)
        if created or reset:
            stdout.write("Setting %s=%s" % (setting[0], setting[1]))
            config.value = setting[1]
            config.save()
