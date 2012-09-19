from Map.models import *
from core.models import SystemData
import json
import datetime
import pytz


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
    for group in user.groups:
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


def add_wormhole_to_map(user, map, topSystem, topType, bottomType, bottomSystem=None,
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

def get_systems_json(map):
    """Returns a JSON string representing the systems in a map."""
    syslist = []
    for sys in map.systems.all():
        if sys.parentsystem:
            dict = {'name': sys.system.name, 'sysclass': sys.system.sysclass,
                    'friendly': sys.friendlyname, 'interest': sys.interesttime, 
                    'parent': sys.parentsystem.pk, 'id': sys.pk, 
                    'occupied': sys.system.occupied, 'info': sys.system.info, 
                    'security': sys.system.security}
            syslist.append(dict)
        else:
            dict = {'name': sys.system.name, 'sysclass': sys.system.sysclass,
                    'friendly': sys.friendlyname, 'interest': sys.interesttime,
                    'parent': None, 'id': sys.pk,
                    'occupied': sys.system.occupied, 'info': sys.system.info,
                    'security': sys.system.security}
            syslist.append(dict)
    return json.dumps(syslist, sort_keys=True, indent=4)


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
    return json.dumps(whlist, sort_keys=True, indent=4)


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
    children = mapSystem.childsystems..count()
    # Remove our children
    for system in mapSystem.childsystems.all():
        delete_system(system, user)
    # Logs for the logs god
    add_log(user, mapSystem.map, "Removed %s from the map and %s child systems."
            % (mapSystem.system.name, children))
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
            signature.sigtype.shortname, signature.system.name)
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
            signature.sigtype.shortname, signature.system.name)

    return None
