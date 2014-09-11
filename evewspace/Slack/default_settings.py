from core.models import ConfigEntry
import random
import string
#defaults = [("TEST_SETTING", "BOB")]
defaults = [
        ("SLACK_ENABLED", False),
        ("SLACK_SUBDOMAIN", "SLACK"),
        ]

def load_defaults():
    for setting in defaults:
        config = ConfigEntry.objects.get_or_create(name=setting[0], user=None)[0]
        config.value = setting[1]
        config.save()
