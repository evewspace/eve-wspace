from django.apps import AppConfig

class AlertsConfig(AppConfig):
    name = 'Alerts'
    verbose_name = "EVE W-Space Alerts module"

# Register registries provided by this app
import Alerts.method_registry