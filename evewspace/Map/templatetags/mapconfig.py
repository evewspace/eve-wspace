from django import template
from Map.models import Map, Destination, SignatureType, SiteSpawn
from django.contrib.auth.models import Group

register = template.Library()

@register.inclusion_tag('map_settings.html')
def map_global_admin():
    """
    Returns the Map admin panel for the settings page.
    """
    return {'maps': Map.objects.all(), 'destinations': Destination.objects.all(),
            'sigtypes': SignatureType.objects.all(),
            'spawns': SiteSpawn.objects.all()}


@register.inclusion_tag('map_settings_single.html')
def map_settings(subject):
    """
    Returns the config block for a sngle map's general settings.
    """
    return {'map': subject}
