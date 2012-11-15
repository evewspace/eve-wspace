"""
A registry module for registration of searches.

This is based on the registry modules from django_autocomplete_light
"""

from django.db import models
from search_base import SearchBase

class SearchRegistry(dict):
    """
    Dict with methods for handling search registration.
    """
    def __init__(self):
        self._models = {}

    def search_for_model(self, model):
        try:
            return self._models[model]
        except KeyError:
            return
    
    def unregister(self, name):
        search = self[name]
        del self[name]

    def register(self, model, name, search_field, queryset):
        """
        Registers a search on a model.

        This is a simple form of the registry from django_autocomplete_light
        that must be provided with a model, name, and the field on the model
        to search.
        """
        if not issubclass(model, models.Model):
            raise AttributeError
        if not search_field:
            raise AttributeError
        if not name:
            name = '%sSearch' % model.__name__

        base = SearchBase

        try:
            search_model_field = model._meta.get_field(search_field)
        except:
            raise Exception('The provided search field is not defined int he model.')
        if not queryset:
            queryset = model.objects.all()
        baseContext = {'choices': queryset,
                'search_field': search_model_field}

        search = type(name, (base,), baseContext)
        self[search.__name__] = search
        self._models[model] = search

def _autodiscover(registry):
    
    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import app's searches module
        try:
            before_import_registry = copy.copy(registry)
            import_module('%s.searches' % app)
        except:
            registry = before_import_registry
            if module_has_submodule(mod, 'searches'):
                raise
registry = SearchRegistry()

def autodiscover():
    _autodiscover(registry)

def register(model, name, search_field, queryset=None):
    """Proxy for registry register method."""
    return registry.register(model, name, search_field, queryset)
