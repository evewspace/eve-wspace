from Map.models import *
from core.models import SystemData
from django.conf import settings
import json
import datetime
from datetime import timedelta
import pytz
from django.contrib.sites.models import Site

def add_log(user, map, action):
    """Adds a log entry into the MapLog for a map."""
    newLog = MapLog(user=user, map=map, action=action,
            timestamp=datetime.datetime.utcnow().replace(tzinfo=pytz.utc))
    newLog.save()


def check_map_permission(user, map):
    """Checks to see if a user should have access to a map.
    Returns the following access levels:  0 = No Access
    1 = View Access 2 = Change Access

    """
    # Case 1: User is unrestricted and map does not require explicit permissions
    if user.has_perm('Map.map_unrestricted'):
        if map.explicitperms == False:
            return 2
    # Case 2: User is in the map's permissions list
    # Note: We return the highest permission of all entries
    highestperm = 0
    for group in user.groups.all():
        if MapPermission.objects.filter(map=map, group=group).count() > 0:
            perm = MapPermission.objects.get(map=map, group=group).access
            if perm > highestperm:
                highestperm = perm
    # Case 3: User has no permissions for the map
    # highestperm should still be 0, so we return that
    return highestperm


def add_system_to_map(user, map, system, friendlyname, isroot, parent):
    """Adds the provided system to the provided map with the provided
    friendly name. Returns the MapSystem object. If isroot = True, the
    system will not have a parent since it is the root of the map.

    """
    if isroot == True:
        newMapSystem = MapSystem(map=map, system=system, 
                friendlyname=friendlyname, interesttime=None, parentsystem=None)
        newMapSystem.save()
        add_log(user, map, "Added root system: %s" % (system.name))
        return newMapSystem
    if isroot == False:
        newMapSystem = MapSystem(map=map, system=system, 
                friendlyname=friendlyname, interesttime=None, parentsystem=parent)
        newMapSystem.save()
        add_log(user, map, "Added system: %s" % (system.name))
        return newMapSystem


def add_wormhole_to_map(map, topSystem, topType, bottomType, bottomSystem=None, 
        bottomBubbled=False, timeStatus=0, massStatus=0, topBubbled=False):
    """Adds a wormhole to the map given top and bottom MapSystems and 
    wormhole information.
    
    """
    newWormhole = Wormhole(map=map, top=topSystem, bottom=bottomSystem,
            top_type=topType, top_bubbled=topBubbled, bottom_type=bottomType,
            bottom_bubbled=bottomBubbled, time_status=timeStatus,
            mass_status=massStatus)
    newWormhole.save()
    return newWormhole


def get_path_to_map_system(system):
    """Returns a list of MapSystems on the route between the map root and
    the provided MapSystem.

    """
    systemlist = []
    system_walker(system, systemlist)
    return systemlist


def system_walker(system, systemlist):
    """Utility function that recursively walks backward on a map path. It
    looks at a MapSystem's parent and adds the system to systemlist if it has one.
    
    """
    if system.parentsystem:
        systemlist.append(system)
        system_walker(system.parentsystem, systemlist)
    return


def get_system_icon(system, user):
    """Takes a MapSystem and returns the appropriate icon to display on the map
    as a realative URL.

    """
    staticPrefix = "%s%s" % (Site.objects.get_current().domain, settings.STATIC_URL + "images/")
    if user.get_profile().currentsystem == system.system: 
        if user.get_profile().lastactive > datetime.datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(minutes=15):
            return staticPrefix + "mylocation.png"

    if system.stfleets.filter(ended__isnull=True).count() != 0:
        return staticPrefix + "farm.png" 

    if system.system.shipkills + system.system.podkills > 0:
        return staticPrefix + "pvp.png" 

    if system.system.npckills > 15:
        return staticPrefix + "carebears.png"

    return None

def system_to_dict(user, system, levelX, levelY):
    """Takes a MapSystem and X,Y data and returns the dict of information to be passed to 
    the map JS as JSON.

    """
    if system.interesttime:
        interest = True
    else:
        interest = False
    if system.map.systems.filter(interesttime__isnull=False).count() != 0:
        interestsystem = system.map.systems.get(interesttime__isnull=False)

        if system in get_path_to_map_system(interestsystem):
            path = True
        else:
            path = False
    else:
        path = False

    if system.parentsystem:
        parentWH = system.parent_wormholes.get()
        result = {'sysID': system.system.pk, 'Name': system.system.name, 'LevelX': levelX,
                'LevelY': levelY, 'SysClass': system.system.sysclass, 
                'Friendly': system.friendlyname, 'interest': interest,
                'interestpath': path, 'ParentID': system.parentsystem.pk, 
                'activePilots': system.system.activepilots.count(),
                'WhToParent': parentWH.bottom_type.name,
                'WhFromParent': parentWH.top_type.name,
                'WhMassStatus': parentWH.mass_status,
                'WhTimeStatus': parentWH.time_status,
                'WhToParentBubbled': parentWH.bottom_bubbled,
                'WhFromParentBubbled': parentWH.top_bubbled,
                'imageURL': get_system_icon(system, user),
                'msID': system.pk}
    else:
        result = {'sysID': system.system.pk, 'Name': system.system.name, 'LevelX': levelX,
                'LevelY': levelY, 'SysClass': system.system.sysclass,
                'Friendly': system.friendlyname, 'interest': interest,
                'interestpath': path, 'ParentID': None, 
                'activePilots': system.system.activepilots.count(),
                'WhToParent': "", 'WhFromParent': "",
                'WhMassStatus': None, 'WhTimeStatus': None,
                'WhToParentBubbled': None, 'WhFromParentBubbled': None,
                'imageURL': get_system_icon(system, user),
                'msID': system.pk}
    return result


def get_systems_json(map, user):
    """Returns a JSON string representing the systems in a map."""
    syslist = []
    root = map.systems.get(parentsystem__isnull=True)
    levelY = 0
    levelX = 0
    syslist.append(system_to_dict(user, root, levelX, levelY))
    recursive_system_data_generator(user, root.childsystems.all(), levelY, levelX +1, syslist)
    return json.dumps(syslist, sort_keys=True)


def recursive_system_data_generator(user, mapSystems, levelY, levelX, syslist):
    """Prepares a list of MapSystem objects for conversion to JSON for map JS.
    Takes a queryset of MapSystems, a levelY integer that is manipulated,
    a levelX integer, and the current list of systems prepared for JSON.

    """
    # We will need an index later, so let's enumerate the mapSystems
    enumSystems = enumerate(mapSystems, start=0)
    for item in enumSystems:
        i = item[0]
        system = item[1]
        if i > 0:
            levelY += 1
        syslist.append(system_to_dict(user, system, levelX, levelY))
        recursive_system_data_generator(user, system.childsystems.all(), levelY, levelX + 1, syslist)


def get_wormholes_json(map):
    """Returns a JSON string representing the wormholes in a map."""
    whlist = []
    for wh in map.wormholes.all():
        if wh.bottom:
            dict = {'whID': wh.pk, 'topID': wh.top.pk, 'topName': wh.top.system.name,
                    'topBubbled': wh.top_bubbled, 'bottomID': wh.bottom.pk,
                    'bottomName': wh.bottom.system.name, 'bottomBubbled': wh.bottom_bubbled,
                    'topType': wh.top_type.name, 'bottomType': wh.bottom_type.name,
                    'time': wh.time_status, 'mass': wh.mass_status,
                    'bottomLife': wh.bottom_type.lifetime, 
                    'bottomJumpMass': wh.bottom_type.jumpmass,
                    'bottomMaxMass': wh.bottom_type.maxmass,
                    'bottomTarget': wh.bottom_type.target,
                    'topLife': wh.top_type.lifetime,
                    'topJumpMass': wh.top_type.jumpmass,
                    'topMaxMass': wh.top_type.maxmass,
                    'topTarget': wh.top_type.target}
            whlist.append(dict)
        else:
            dict = {'whID': wh.pk, 'topID': wh.top.pk, 'topName': wh.top.system.name,
                    'topBubbled': wh.top_bubbled, 'bottomID': None,
                    'bottomName': None, 'bottomBubbled': None,
                    'topType': wh.top_type.name, 'bottomType': None,
                    'time': wh.time_status, 'mass': wh.mass_status,
                    'bottomLife': None, 'bottomJumpMass': None,
                    'bottomMaxMass': None, 'bottomTarget': None,
                    'topLife': wh.top_type.lifetime,
                    'topJumpMass': wh.top_type.jumpmass,
                    'topMaxMass': wh.top_type.maxmass,
                    'topTarget': wh.top_type.target}
            whlist.append(dict)
    return json.dumps(whlist, sort_keys=True)


def delete_system(mapSystem, user):
    """Recursively deletes a system from the map along with any wormhole
    connections. Takes a MapSystem and a user."""
    # Make sure we're not trying to delete the root system.
    if mapSystem.map.root == mapSystem.system:
        return {"errors": "You are trying to delete the root system, please delete the map instead."}
    # If we're the only instance of this system, remove sigs
    if mapSystem.system.maps.count() == 1:
        mapSystem.system.signatures.all().delete()
    # Remove our parent wormholes
    mapSystem.parent_wormholes.all().delete()
    # Get a child count before we kill them all
    children = mapSystem.childsystems.count()
    # Remove our children
    for system in mapSystem.childsystems.all():
        delete_system(system, user)
    # Logs for the logs god
    delSystemname = mapSystem.system.name
    mapSystem.delete()
    add_log(user, mapSystem.map, "Removed %s from the map and %s child systems."
            % (delSystemname, children))
    return None


def add_signature(system, user, sigtype, sigid):
    """Adds a signature to a system. Takes System, user, signaturetype
        and signature id.

    """
    newSig = Signature(system=system, sigtype=sigtype, sigid=sigid,
            updated=True, activated=None, downtimes=0, ratscleared=None,
            lastescalated=None)
    newSig.save()
    # Systems may be in multiple maps, so add log for all of them
    for map in system.maps.all():
        add_log(user, map, "Added signature %s (%s) in %s." 
                % (sigid, sigtype, system.name))
    return None


def delete_signature(signature, user):
    """Removes a signature from a system."""
    signature.delete()

    for map in signature.system.maps.all():
        add_log(user, map, "Deleted signature %s (%s) in %s." 
                % (signature.sigid, signature.sigtype.shortname, signature.system.name))
    return None


def escalate_site(signature, user):
    """Marks a site as escalated by setting lastescalated to now.
        If the site hasn't been marked as activated or ratscleared, it is now.

    """
    signature.lastescalated = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

    if signature.activated == None:
        activate_site(signature, user)

    if signature.ratscleared == None:
        clear_rats(signature, user)

    for map in signature.system.maps.all():
        add_log(user, map, "Escalated site %s (%s) in %s." % (signature.sigid, 
            signature.sigtype.shortname, signature.system.name))
    return None


def clear_rats(signature, user):
    """Marks a site as having its rats cleared. Site is marked activated if it
        hasn't been already.

    """
    signature.ratscleared = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

    if signature.activated == None:
        activate_site(signature, user)
    for map in signature.system.maps.all():
        add_log(user, map, "Cleared rats from site %s (%s) in %s."
            % (signature.sigid, signature.sigtype.shortname, signature.system.name))

    return None


def activate_site(signature, user):
    """Marks a site as having been activated."""

    signature.activated = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

    for map in signature.system.maps.all():
        add_log(user, map, "Activated site %s (%s) in %s." % (signature.sigid, 
            signature.sigtype.shortname, signature.system.name))

    return None


def get_map_context(map, user):
    """Gets the context dict items needed to render the map. Used for both
        initial map view and system-specific views.

    """
    permissions = check_map_permission(user, map)
    systemsJSON = get_systems_json(map, user)
    wormholesJSON = get_wormholes_json(map)

    context = {'map': map, 'access': permissions, 'systemsJSON': systemsJSON, 
            'wormholesJSON': wormholesJSON}
    return context


def get_wormhole_type(system1, system2):
    """Gets the one-way wormhole types between system1 and system2."""
    
    source = "K"
    destination = "K"
    # Set the source and destination for system1 > system2
    if system1.sysclass < 7:
        source = str(system1.sysclass)
    if system1.sysclass == 7:
        source = "H"
    if system1.sysclass > 7:
        source = "NH"
    
    destination = system2.sysclass
    
    sourcewh = None

    if source == "H":
        if WormholeType.objects.filter(source="H",
                destination=destination).count() == 0:
            sourcewh = WormholeType.objects.filter(source="K",
                    destination=destination).all()
        else:
            sourcewh = WormholeType.objects.get(source="H",
                    destination=destination)
    if source == "NH":
        if WormholeType.objects.filter(source="NH",
                destination=destination).count() == 0:
            sourcewh = WormholeType.objects.filter(source="K",
                    destination=destination).all()
        else:
            sourcewh = WormholeType.objects.filter(source="NH",
                    destination=destination).all()
    if source == "5" or source == "6":
        if WormholeType.objects.filter(source="Z",
                destination=destination).count() != 0:
            sourcewh = WormholeType.objects.filter(source="Z",
                    destination=destination).all
    
    if sourcewh == None:
        sourcewh = WormholeType.objects.filter(source=source,
                destination=destination).all()
    return sourcewh


def get_possible_wormhole_types(system1, system2):
    """Takes two systems and gets the possible wormhole types between them.
    For example, given system1 as highsec and system2 as C2, it should return
    R943 and B274. system1 is the source and system2 is the destination.
    Results are returned as lists because some combinations have multiple possibilities.
    Returns a dict in the format {system1: [R943,], system2: [B274,]}.

    """

    # Get System1 > System2

    forward = get_wormhole_type(system1, system2)
    
    # Get Reverse

    reverse = get_wormhole_type(system2, system1)

    result = {'system1': forward, 'system2': reverse}

    return result


def system_is_in_map(system, map):
    """Returns true if a System is a MapSystem in the map."""
    if map.systems.filter(system=system).count() != 0:
        return True
    else:
        return False

