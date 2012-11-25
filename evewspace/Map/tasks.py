from celery import task
from Map.models import System, KSystem, Signature
from core.models import Faction
from POS.models import Alliance
import eveapi
from API import utils as handler
from django.core.cache import cache

@task()
def update_system_stats():
    """
    Updates the System Statistics (jumps, kills) from the API.
    """
    api = eveapi.EVEAPIConnection(cacheHandler=handler)
    jumpapi = api.map.Jumps()
    killapi = api.map.Kills()
    System.objects.all().update(shipkills=0, podkills=0, npckills=0)
    KSystem.objects.all().update(jumps=0)
    # Update jumps from Jumps API for K-space systems
    for entry in jumpapi.solarSystems:
        try:
            sys = KSystem.objects.get(pk=entry.solarSystemID)
            sys.jumps = entry.shipJumps
            sys.save()
        except:
            pass
    # Update kills from Kills API
    for entry in killapi.solarSystems:
        try:
            sys = System.objects.get(pk=entry.solarSystemID)
            sys.shipkills = entry.shipKills
            sys.podkills = entry.podKills
            sys.npckills = entry.factionKills
            sys.save()
        except:
            pass

@task()
def update_system_sov():
    """
    Updates the Sov for K-Space systems. If any exceptions are raised 
    (e.g. Alliance record doesn't exist), sov is just marked "None."
    """
    api = eveapi.EVEAPIConnection(cacheHandler=handler)
    sovapi = api.map.Sovereignty()
    KSystem.objects.all().update(sov="None")
    for sys in sovapi.solarSystems:
        try:
            system = KSystem.objects.get(pk=sys.solarSystemID)
            if sys.factionID:
                system.sov = Faction.objects.get(pk=sys.factionID).name
                system.save()
            elif sys.allianceID:
                system.sov = Alliance.objects.get(pk=sys.allianceID).name
                system.save()
        except:
            pass

@task()
def fill_jumps_cache():
    """
    Ensures that the jumps cache is filled.
    """
    if not cache.get('sysJumps'):
        for sys in KSystem.objects.all():
            cache.set(sys.pk, [i.tosystem for i in SystemJump.objects.filter(
                fromsystem=sys.pk).all()])
        cache.set('sysJumps', 1)

@task()
def check_server_status():
    """
    Checks the server status, if it detects the server is down, set updated=False
    on all signatures.
    """
    api = eveapi.EVEAPIConnection(cacheHandler=handler)
    try:
        statusapi = api.server.ServerStatus()
    except:
        # API is down, assume the server is down as well
        Signature.objects.all().update(updated=False)
        return
    if statusapi.serverOpen == u'True':
        return
    Signature.objects.all().update(updated=False)
