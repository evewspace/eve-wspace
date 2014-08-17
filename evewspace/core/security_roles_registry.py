from core.models import SecurityRole
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule

def autodiscover_roles():
    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        try:
            role_registry = import_module('%s.security_roles' % app)
            # Roles should be declared as a tuple of name, description
            for role in role_registry.roles:
                if not SecurityRole.objects.filter(app=app,
                        name=role[0]).exists():
                    SecurityRole(app=app, name=role[0],
                            description=role[1]).save()
        except:
            if module_has_submodule(mod, 'security_roles'):
                raise
