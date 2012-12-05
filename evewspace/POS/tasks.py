from celery import task
from POS.models import Alliance, Corporation
import eveapi
from API import utils as handler

@task()
def update_alliance(allianceID):
    """
    Updates an alliance and it's corporations from the API.
    """
    api = eveapi.EVEAPIConnection(cacheHandler=handler)
    allianceapi = api.eve.AllianceList().alliances.Get(allianceID)
    if Alliance.objects.filter(id=allianceID).count():
        # Alliance exists, update it
        for corp in allianceapi.memberCorporations:
            update_corporation(corp.corporationID)
        alliance = Alliance.objects.get(id=allianceID)
        alliance.name = allianceapi.name
        alliance.shortname = allianceapi.shortName
        # Check to see if we have a record for the executor
        if Corporation.objects.filter(id=allianceapi.executorCorpID).count():
            alliance.executor = Corporation.objects.get(id=allianceapi.executorCorpID)
    else:
        # Alliance doesn't exists, add it without executor, update corps
        # and then update the executor
        alliance = Alliance(id=allianceapi.allianceID, name=allianceapi.name,
                shortname=allianceapi.shortName, executor=None)
        alliance.save()
        for corp in allianceapi.memberCorporations:
            update_corporation(corp.corporaitonID)
        try:
            # If an alliance's executor can't be processed for some reason,
            # set it to None
            alliance.executor = Corporation.objects.get(id=allianceapi.executorCorpID)
        except:
            alliance.executor = None
        alliance.save()

@task()
def update_corporation(corpID):
    """
    Updates a corporation from the API. If it's alliance doesn't exist,
    update that as well.
    """
    api = eveapi.EVEAPIConnection(cacheHandler=handler)
    # Encapsulate this in a try block because one corp has a fucked
    # up character that chokes eveapi
    try:
        corpapi = api.corp.CorporationSheet(corporationID=corpID)
    except:
        raise AttributeError("Invalid Corp ID")

    if corpapi.allianceID:
        try:
            alliance = Alliance.objects.get(id=corpapi.allianceID)
        except:
            # If the alliance doesn't exist, we start a task to add it
            # and terminate this task since the alliance task will call
            # it after creating the alliance object
            update_alliance.delay(corpapi.allianceID)
            return
    else:
        alliance = None

    if Corporation.objects.filter(id=corpID).count():
        # Corp exists, update it
        corp = Corporation.objects.get(id=corpID)
        corp.member_count = corpapi.memberCount
        corp.ticker = corpapi.ticker
        corp.name = corpapi.corporationName
        corp.alliance = alliance
        corp.save()
    else:
        # Corp doesn't exist, create it
        corp = Corporation(id=corpID, member_count=corpapi.memberCount,
                name=corpapi.corporationName, alliance=alliance)
        corp.save()
    return corp

@task()
def update_all_alliances():
    """
    Updates all corps in all alliances. This task will take a long time
    to run.
    """
    api = eveapi.EVEAPIConnection(cacheHandler=handler)
    alliancelist = api.eve.AllianceList()
    for alliance in alliancelist.alliances:
        update_alliance(alliance.allianceID)
