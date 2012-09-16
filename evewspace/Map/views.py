from Map.models import *
from Map.utils import *
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime
import pytz
# Create your views here.

@login_required()
def get_map(request, mapID="0"):
    """This function takes a request and Map ID, determines if access
    should be permitted and either builds a context and loads map.html
    or raises a 403 error. If the map does not exist, we go back to home.
    """
    # If mapID is 0, then a map ID was not passed and we should direct to home
    if mapID == "0":
        return HttpResponseRedirect(reverse('core.views.home_view'))
    # Get the map if it exists. If it doesn't go t`o home page.

    try:
        result = Map.objects.get(pk=mapID)
    except Map.DoesNotExist:
        return HttpResponseRedirect(reverse('core.views.home_view'))
    # Check our access for the map. If 0, raise PermissionDenied.
    permissions = check_map_permission(request.user, result)
    if permissions == 0:
        return HttpResponseRedirect(reverse('core.views.home_view'))
    # Build the context dict and render map.html template
    context = {'map': result, 'access': permissions,}
    return TemplateResponse(request, 'map.html', context)


@permission_required('Map.add_Map')
def create_map(request):
    """This function creates a map and then redirects to the new map.

    """
    if request.method == 'POST':
        form = MapForm(request.POST)
        if form.is_valid():
            newMap = form.save()
            add_log(request.user, newMap, "Created the %s map." % (newMap.name))
            add_system_to_map(request.user, newMap, newMap.root, "Root", True, None)
            return HttpResponseRedirect(reverse('Map.views.get_map', kwargs={'mapID': newMap.pk, }))
    else:
        form = MapForm
        return TemplateResponse(request, 'new_map.html', { 'form': form, })

