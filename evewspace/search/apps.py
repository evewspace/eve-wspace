from django.apps import AppConfig

from . import registry

class SearchConfig(AppConfig):
    name = 'search'
    verbose_name = "EVE W-Space search module"

    def ready(self):
        registry.autodiscover()
