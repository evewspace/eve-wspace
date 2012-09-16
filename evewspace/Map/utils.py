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
            dict = {'topID': wh.top.pk, 'topName': wh.top.system.name,
                    'topBubbled': wh.topbubbled, 'bottomID': wh.bottom.pk,
                    'bottomName': wh.bottom.system.name, 'bottomBubbled': wh.bottom_bubbled,
                    'topType': wh.top_type, 'bottomType': wh.bottom_type,
                    'time': wh.time_status, 'mass': wh.mass_status}
            whlist.append(dict)
        else:
            dict = {'topID': wh.top.pk, 'topName': wh.top.system.name,
                    'topBubbled': wh.topbubbled, 'bottomID': None,
                    'bottomName': None, 'bottomBubbled': None,
                    'topType': wh.top_type, 'bottomType': None,
                    'time': wh.time_status, 'mass': wh.mass_status}
            whlist.append(dict)
    return json.dumps(whlist, sort_keys=True, indent=4)
