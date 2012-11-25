from POS.models import *
from Map.models import System
from core.models import Type
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta
import pytz
import eveapi
from API import utils as handler
from POS import tasks

@login_required
def test_fit(request, posID):
    """
    Temporary test method for filling a POS fit from DScan.
    """
    pos = get_object_or_404(POS, pk=posID)
    if request.method == "POST":
        data = request.POST['fit'].encode('utf-8')
        pos.fit_from_dscan(data)
        return HttpResponse('[]')
    else:
        return TemplateResponse(request, 'testfitter.html', {'pos': pos})

@permission_required('POS.delete_pos')
def remove_pos(request, sysID,  posID):
    """
    Removes the POS. Raises PermissionDenied if it is a CorpPOS.
    """
    if not request.is_ajax():
        raise PermissionDenied

    pos = get_object_or_404(POS, pk=posID)
    if CorpPOS.objects.filter(pk=posID).count():
        raise PermissionDenied

    pos.delete()
    return HttpResponse('[]')


@login_required
def get_pos_list(request, sysID):
    if not request.is_ajax():
        raise PermissionDenied
    system = get_object_or_404(System, pk=sysID)
    poses = POS.objects.filter(system=system).all()
    return TemplateResponse(request, 'poslist.html', {'system': system,
        'poses': poses})


@permission_required('POS.edit_pos')
def edit_pos(request, sysID, posID):
    """
    GET gets the edit POS dialog, POST processes it.
    """
    if not request.is_ajax():
        raise PermissionDenied
    system = get_object_or_404(System, pk=sysID)
    pos = get_object_or_404(POS, pk=posID)
    if request.method == 'POST':
        tower = get_object_or_404(Type, name=request.POST['tower'])
        try:
            corp = Corporation.objects.get(name=request.POST['corp'])
        except:
            # Corp isn't in our DB, get its ID and add it
            try:
                api = eveapi.EVEAPIConnection(cacheHandler=handler)
                corpID = api.eve.CharacterID(names=request.POST['corp']).characters[0].characterID
                result = tasks.update_corporation.delay(corpID)
                corp = result.get()
            except:
                # The corp doesn't exist
                raise Http404
        pos.corporation = corp
        pos.towertype = tower
        pos.posname = request.POST['name']
        pos.planet = int(request.POST['planet'])
        pos.moon = int(request.POST['moon'])
        pos.status = int(request.POST['status'])
        pos.fitting = request.POST['fitting']

        # Have the async worker update the corp just so that it is up to date
        tasks.update_corporation.delay(corp.id)
        if pos.status == 3:
            delta = timedelta(days=int(request.POST['rfdays']), 
                    hours=int(request.POST['rfhours']),
                    minutes=int(request.POST['rfminutes']))
            pos.rftime = datetime.now(pytz.utc) + delta
        pos.save()
        if request.POST.get('dscan', None) == "1":
            pos.fit_from_dscan(request.POST['fitting'].encode('utf-8'))
        return HttpResponse('[]')
    else:
        fitting = pos.fitting.replace("<br />", "\n")
        return TemplateResponse(request, 'edit_pos.html', {'system': system, 
            'pos': pos, 'fitting': fitting})


@permission_required('POS.add_pos')
def add_pos(request, sysID):
    """
    GET gets the add POS dialog, POST processes it.
    """
    if not request.is_ajax():
        raise PermissionDenied

    system = get_object_or_404(System, pk=sysID)
    if request.method == 'POST':
        tower = get_object_or_404(Type, name=request.POST['tower'])
        try:
            corp = Corporation.objects.get(name=request.POST['corp'])
        except:
            # Corp isn't in our DB, get its ID and add it
            try:
                api = eveapi.EVEAPIConnection(cacheHandler=handler)
                corpID = api.eve.CharacterID(names=request.POST['corp']).characters[0].characterID
                result = tasks.update_corporation.delay(corpID)
                corp = result.get()
            except:
                # The corp doesn't exist
                raise Http404
        pos=POS(system=system, planet=int(request.POST['planet']),
                moon=int(request.POST['moon']), towertype=tower,
                posname=request.POST['name'], fitting=request.POST['fitting'],
                status=int(request.POST['status']), corporation=corp)
        # Have the async worker update the corp just so that it is up to date
        tasks.update_corporation.delay(corp.id)
        if pos.status == 3:
            delta = timedelta(days=int(request.POST['rfdays']), 
                    hours=int(request.POST['rfhours']),
                    minutes=int(request.POST['rfminutes']))
            pos.rftime = datetime.now(pytz.utc) + delta
        pos.save()

        if request.POST.get('dscan', None) == "1":
            pos.fit_from_dscan(request.POST['fitting'].encode('utf-8'))
        return HttpResponse('[]')
    else:
        return TemplateResponse(request, 'add_pos.html', {'system': system})
