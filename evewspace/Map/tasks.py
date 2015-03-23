#   Eve W-Space
#   Copyright 2014 Andrew Austin and contributors
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from datetime import datetime, timedelta

from celery import task
from Map.models import System, KSystem, Signature
from core.models import Faction
import eveapi
from API import cache_handler as handler
from django.core.cache import cache
import pytz


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
            KSystem.objects.filter(pk=entry.solarSystemID).update(
                jumps=entry.shipJumps)
        except Exception:
            pass
    # Update kills from Kills API
    for entry in killapi.solarSystems:
        try:
            System.objects.filter(pk=entry.solarSystemID).update(
                shipkills=entry.shipKills,
                podkills=entry.podKills,
                npckills=entry.factionKills
            )
        except Exception:
            pass


@task()
def update_system_sov():
    """
    Updates the Sov for K-Space systems. If any exceptions are raised
    (e.g. Alliance record doesn't exist), sov is just marked "None."
    """
    api = eveapi.EVEAPIConnection(cacheHandler=handler)
    sovapi = api.map.Sovereignty()
    alliance_list = api.eve.AllianceList().alliances
    lookup_table = {}
    for alliance in alliance_list:
        lookup_table[alliance.allianceID] = alliance.name
    KSystem.objects.all().update(sov="None")
    for sys in sovapi.solarSystems:
        try:
            if sys.factionID:
                KSystem.objects.filter(pk=sys.solarSystemID).update(
                    sov=Faction.objects.get(pk=sys.factionID).name)
            elif sys.allianceID:
                if sys.allianceID in lookup_table:
                    KSystem.objects.filter(pk=sys.solarSystemID).update(
                        sov=lookup_table[sys.allianceID])
        except Exception:
            pass


@task()
def fill_jumps_cache():
    """
    Ensures that the jumps cache is filled.
    """
    if not cache.get('route_graph'):
        from Map.utils import RouteFinder

        rf = RouteFinder()
        # Initializing RouteFinder should be sufficient to cache the graph
        # If it doesn't for some reason, we explicitly cache it
        if not cache.get('route_graph'):
            rf._cache_graph()


@task()
def check_server_status():
    """
    Checks the server status, if it detects the server is down,
    set updated=False on all signatures. This is deprecated as of Hyperion and
    is maintained to prevent older configuration files from breaking on upgrade.
    """
    return None


@task()
def downtime_site_update():
    """
    This task should be run during the scheduled EVE downtime.
    It triggers the increment_downtime function on all singatures
    that have been activated.
    """
    for sig in Signature.objects.all():
        if sig.downtimes or sig.downtimes == 0:
            sig.increment_downtime()


@task()
def clear_stale_records():
    """
    This task will clear any user location records older than 15 minutes.
    """
    limit = datetime.now(pytz.utc) - timedelta(minutes=15)
    Signature.objects.filter(owned_time__isnull=False,
                             owned_time__lt=limit).update(owned_time=None,
                                                          owned_by=None)
