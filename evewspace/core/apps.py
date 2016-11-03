from django.apps import AppConfig

from .registry import Registry

class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = "EVE W-Space core module"

    def ready(self):
        Registry._autodiscover_all()
        Registry._deebug_print_registry()

# Load registries provided by this module
import core.nav_registry
import core.admin_page_registry