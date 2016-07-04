from django.apps import AppConfig

class AccountConfig(AppConfig):
    name = 'account'
    verbose_name = "EVE W-Space account module"

# Register registries provided by this app
import account.profile_section_registry
import account.group_admin_section_registry
import account.user_admin_section_registry