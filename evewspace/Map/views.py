from Map.models import *
from Map import utils
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from datetime import datetime, timedelta
import pytz
import json

# Decorator to check map permissions. Takes request and mapID
# Permissions are 0 = None, 1 = View, 2 = Change
# When used without a permission=x specification, requires Change access

def require_map_permission(permission=2):
    def _dec(view_func):
        def _view(request, mapID, *args, **kwargs):
            map = get_object_or_404(Map, pk=mapID)
            if utils.check_map_permission(request.user, map) < permission:
                raise PermissionDenied
            else:
                return view_func(request, mapID, *args, **kwargs)
        _view.__name__ = view_func.__name__
        _view.__doc__ = view_func.__doc__
        _view.__dict__ = view_func.__dict__
        return _view
    return _dec

@login_required
@require_map_permission(permission=1)
def get_map(request, mapID):
    """Get the map and determine if we have permissions to see it. 
    If we do, then return a TemplateResponse for the map. If map does not
    exist, return 404. If we don't have permission, return PermissionDenied.
    """
    map = get_object_or_404(Map, pk=mapID)
    context = utils.get_map_context(map, request.user)
    return TemplateResponse(request, 'map.html', context)


@login_required
@require_map_permission(permission=1)
def map_checkin(request, mapID):
    # Initialize json return dict
    jsonvalues = {}
    profile = request.user.get_profile()
    currentmap = get_object_or_404(Map, pk=mapID)

    # Out AJAX requests should post a JSON datetime called loadtime
    # back that we use to get recent logs.
    if  'loadtime' not in request.POST:
        return HttpResponse(json.dumps({error: "No loadtime"}),mimetype="application/json")
    timestring = request.POST['loadtime']

    if request.is_igb:
        loadtime = datetime.strptime(timestring, '%Y-%m-%dT%H:%M:%SZ')
        loadtime = loadtime.replace(tzinfo=pytz.utc)
    else:
        loadtime = datetime.strptime(timestring, '%Y-%m-%dT%H:%M:%S.%fZ')
        loadtime.replace(tzinfo=pytz.utc)

    if request.is_igb_trusted:
        dialogHtml = checkin_igb_trusted(request, currentmap)
        if dialogHtml is not None:
            jsonvalues.update({'dialogHTML': dialogHtml})

    newlogquery = MapLog.objects.filter(timestamp__gt=loadtime)
    loglist = []

    for log in newlogquery:
        loglist.append("Time: %s  User: %s Action: %s" % (log.timestamp,
            log.user.username, log.action))

    logstring = render_to_string('log_div.html', {'logs': loglist})
    jsonvalues.update({'logs': logstring})

    return HttpResponse(json.dumps(jsonvalues), mimetype="application/json")

def checkin_igb_trusted(request, map):
    """
    Runs the specific code for the case that the request came from an igb that
    trusts us, returns None if no further action is required, returns a string
    containing the html for a system add dialog if we detect that a new system
    needs to be added
    """
    profile = request.user.get_profile()
    currentsystem = System.objects.get(name=request.eve_systemname)
    oldsystem = None
    result = None
    
    if profile.currentsystem:
        oldsystem = profile.currentsystem

    #Conditions for the system to be automagically added to the map. The case
    #of oldsystem == None is handled by a condition on "sys in map" (None cannot
    #be in any map), the case oldsystem == currentsystem is handled by the
    #condition that if two systems are equal one cannot be in and the other not
    #in the same map (i.e 'oldsystem in map and currentsystem not in map' will be
    #False).
    if (
      oldsystem in map
      and currentsystem not in map
      #Stop it from adding everyone's paths through k-space to the map
      and not (oldsystem.is_kspace() and currentsystem.is_kspace())
      and profile.lastactive > datetime.now(pytz.utc) - timedelta(minutes=5)
      ):
        context = { 'oldsystem' : oldsystem, 
                    'newsystem' : currentsystem,
                    'wormhole'  : util.get_possible_wh_types(oldsystem, currentsystem),
                  }
        result = render_to_string('igb_system_add_dialog.html', context,
                                  context_instance=RequestContext(request))

    profile.update_location(currentsystem)
    return result

def get_system_context(msID):
    mapsys = get_object_or_404(MapSystem, pk=msID)
    currentmap = mapsys.map

    #if mapsys represents a k-space system get the relevent KSystem object
    if mapsys.system.is_kspace():
        system = mapsys.system.ksystem
    #otherwise get the relevant WSystem
    else:
        system = mapsys.system.wsystem

    scanthreshold = datetime.now(pytz.utc) - timedelta(hours=3)
    interestthreshold = datetime.now(pytz.utc) - timedelta(minutes=settings.MAP_INTEREST_TIME)

    scanwarning = system.lastscanned < scanthreshold
    interest = mapsys.interesttime and mapsys.interesttime > interestthreshold

    return { 'system' : system, 'mapsys' : mapsys, 
             'scanwarning' : scanwarning, 'isinterest' : interest }

    
@login_required
@require_map_permission(permission=2)
def add_system(request, mapID):
    """
    AJAX view to add a system to a map. Requires POST containing:
       topMsID: MapSystem ID of the parent MapSystem
       bottomSystem: Name of the new system
       topType: WormholeType name of the parent side
       bottomType: WormholeType name of the new side
       timeStatus: Womrhole time status integer value
       massStatus: Wormhole mass status integer value
       topBubbled: 1 if Parent side bubbled
       bottomBubbled: 1 if new side bubbled
       friendlyName: Friendly name for the new MapSystem
    """
    if not request.is_ajax():
       raise PermissionDenied
    try:
        # Prepare data
        map = Map.objects.get(pk=mapID)
        topMS = MapSystem.objects.get(pk=request.POST.get('topMsID'))
        bottomSys = System.objects.get(name=request.POST.get('bottomSystem'))
        topType = WormholeType.objects.get(name=request.POST.get('topType'))
        bottomType = WormholeType.objects.get(name=request.POST.get('bottomType'))
        timeStatus = int(request.POST.get('timeStatus'))
        massStatus = int(request.POST.get('massStatus'))
        topBubbled = "1" == request.POST.get('topBubbled')
        bottomBubbled = "1" == request.POST.get('bottomBubbled')
        # Add System
        bottomMS = utils.add_system_to_map(request.user, map, bottomSys,
                request.POST.get('friendlyName'), False, topMS)
        # Add Wormhole
        utils.add_wormhole_to_map(map, topMS, topType, bottomType, bottomMS,
                                  bottomBubbled, timeStatus, massStatus, topBubbled)

        return HttpResponse('[]')
    except ObjectDoesNotExist:
        return HttpResponse(status=400)


@login_required
@require_map_permission(permission=1)
def system_details(request, mapID, msID):
    """
    Returns a html div representing details of the System given by msID in
    map mapID
    """
    if not request.is_ajax():
        raise PermissionDenied

    return render(request, 'system_details.html', get_system_context(msID))

@login_required
@require_map_permission(permission=1)
def system_menu(request, mapID, msID):
    """
    Returns the html for system menu
    """
    if not request.is_ajax():
        raise PermissionDenied

    return render(request, 'system_menu.html', get_system_context(msID))

@login_required
@require_map_permission(permission=1)
def system_tooltip(request, mapID, msID):
    """
    Returns a system tooltip for msID in mapID
    """
    if not request.is_ajax():
        raise PermissionDenied

    return render(request, 'system_tooltip.html', get_system_context(msID))


@login_required
@require_map_permission(permission=1)
def wormhole_tooltip(request, mapID, whID):
    """Takes a POST request from AJAX with a Wormhole ID and renders the
    wormhole tooltip for that ID to response.
    
    """
    if request.is_ajax():
        wh = get_object_or_404(Wormhole, pk=whID)
        return HttpResponse(render_to_string("wormhole_tooltip.html",
            {'wh': wh}, context_instance=RequestContext(request)))
    else:
        raise PermissionDenied


@login_required()
@require_map_permission(permission=2)
def mark_scanned(request, mapID, msID):
    """Takes a POST request from AJAX with a system ID and marks that system
    as scanned.

    """
    if request.is_ajax():
        mapsys = get_object_or_404(MapSystem, pk=msID)
        mapsys.system.lastscanned = datetime.now(pytz.utc)
        mapsys.system.save()
        return HttpResponse('[]')
    else:
        raise PermissionDenied


@login_required()
def manual_location(request, mapID, msID):
    """Takes a POST request form AJAX with a System ID and marks the user as
    being active in that system.

    """
    if request.is_ajax():
        mapsystem = get_object_or_404(MapSystem, pk=msID)
        utils.assert_location(request.user, mapsystem.system)
        return HttpResponse("[]")
    else:
        raise PermissionDenied


@login_required()
@require_map_permission(permission=2)
def set_interest(request, mapID, msID):
    """Takes a POST request from AJAX with an action and marks that system
    as having either utcnow or None as interesttime. The action can be either 
    "set" or "remove".

    """
    if request.is_ajax():
        action = request.POST.get("action","none")
        if action == "none":
            raise Http404
        system = get_object_or_404(MapSystem, pk=msID)
        if action == "set":
            system.interesttime = datetime.now(pytz.utc)
            system.save()
            return HttpResponse('[]')
        if action == "remove":
            system.interesttime = None
            system.save()
            return HttpResponse('[]')
        return HttpResponse(staus=418)
    else:
        raise PermissionDenied

@login_required()
@require_map_permission(permission=2)
def add_signature(request, mapID, msID):
    """This function processes the Add Signature form. GET gets the form
    and POST submits it and returns either a blank JSON list or a form with errors.
    in addition to the SignatureForm, the form should have a hidden field called sysID
    with the System id. All requests should be AJAX.
    
    """
    if not request.is_ajax():
        raise PermissionDenied

    if request.method == 'POST':
        form = SignatureForm(request.POST)
        mapsystem = get_object_or_404(MapSystem, pk=msID)
        if form.is_valid():
            newSig = form.save(commit=False)
            newSig.system = mapsystem.system
            newSig.updated = True
            newSig.save()
            return HttpResponse('[]')
        else:
            return TemplateResponse(request, "add_sig_form.html", {'form': form})
    else:
        form = SignatureForm()
    return TemplateResponse(request, "add_sig_form.html", {'form': form})


@login_required()
def get_signature_list(request, mapID, msID):
    raise PermissionDenied


@login_required
@require_map_permission(permission=2)
def edit_wormhole(request, whID):
    raise PermissiondDenied


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
            return HttpResponseRedirect(reverse('Map.views.get_map', 
                kwargs={'mapID': newMap.pk }))
    else:
        form = MapForm
        return TemplateResponse(request, 'new_map.html', { 'form': form, })

