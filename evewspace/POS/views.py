from POS.models import *
from Map.models import System
from core.models import Type
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from datetime import datetime
import pytz
import eveapi
from API import utils as handler

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
