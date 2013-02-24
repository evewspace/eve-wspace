#    Eve W-Space
#    Copyright (C) 2013  Andrew Austin and other contributors
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version. An additional term under section
#    7 of the GPL is included in the LICENSE file.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# Create your views here.
from models import Fleet, UserLog, SiteType, SiteRecord, UserSite
from Map.models import System
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from datetime import datetime
import pytz
import csv

def require_boss():
    def _dec(view_func):
        def _view(request, fleetID, *args, **kwargs):
            fleet = get_object_or_404(Fleet, pk=fleetID)
            if fleet.current_boss != request.user or fleet.ended:
                raise PermissionDenied
            else:
                return view_func(request, fleetID, *args, **kwargs)
        _view.__name__ = view_func.__name__
        _view.__doc__ = view_func.__doc__
        _view.__dict__ = view_func.__dict__
        return _view
    return _dec


@permission_required('SiteTracker.can_sitetracker')
def status_bar(request):
    """
    Return a template with just the ST status bar tag.
    """
    return TemplateResponse(request, 'st_bar_refresh.html')

@permission_required('SiteTracker.can_sitetracker')
def create_fleet(request):
    """
    Takes a system ID via POST and makes a sitetracker fleet with the
    requesting user as initial and current boss. Then adds the requestor
    to the fleet as a member.
    """
    if not request.is_ajax():
        raise PermissionDenied
    sysid = request.POST.get('sysID', None)
    system = get_object_or_404(System, pk=sysid)
    fleet = Fleet(initial_boss=request.user, current_boss=request.user,
            system=system)
    fleet.save()
    UserLog(fleet=fleet, user=request.user).save()
    return HttpResponse()


@permission_required('SiteTracker.can_sitetracker')
def leave_fleet(request, fleetID=None):
    """
    Leaves the given fleet. If fleetID is not provided, leave all fleets.
    """
    if not request.is_ajax():
        raise PermissionDenied
    if fleetID:
        fleet = get_object_or_404(Fleet, pk=fleetID)
        fleet.leave_fleet(request.user)
        return HttpResponse()
    else:
        for log in request.user.sitetrackerlogs.filter(leavetime=None).all():
            log.fleet.leave_fleet(request.user)
        return HttpResponse()


@require_boss()
def kick_member(request, fleetID, memberID):
    """
    Removes a member from the fleet.
    """
    if not request.is_ajax():
        raise PermissionDenied

    fleet = get_object_or_404(Fleet, pk=fleetID)
    member = get_object_or_404(Fleet.members, leavetime=None, user__pk=memberID)
    fleet.leave_fleet(member)
    return HttpResponse()


@permission_required('SiteTracker.can_sitetracker')
def promote_member(request, fleetID, memberID):
    """
    Promote the given member to boss. Boss permisison not required
    since we allow for siezure from an AFK boss.
    """
    if not request.is_ajax():
        raise PermissionDenied

    fleet = get_object_or_404(Fleet, pk=fleetID)
    member = get_object_or_404(User, pk=memberID)
    fleet.make_boss(member)
    return HttpResponse()


@permission_required('SiteTracker.can_sitetracker')
def join_fleet(request, fleetID):
    """
    Join the current user to the fleet.
    """
    if not request.is_ajax():
        raise PermissionDenied

    fleet = get_object_or_404(Fleet, pk=fleetID)
    fleet.join_fleet(request.user)
    return HttpResponse()


@require_boss()
def disband_fleet(request, fleetID):
    """
    Disband the fleet.
    """
    if not request.is_ajax():
        raise PermissionDenied
    fleet = get_object_or_404(Fleet, pk=fleetID)
    fleet.close_fleet()
    return HttpResponse()


@require_boss()
def credit_site(request, fleetID):
    """
    Credit a site to the given fleet. Takes POST input:
        type = short_name of site type
    """
    if not request.is_ajax():
        raise PermissionDenied

    fleet = get_object_or_404(Fleet, pk=fleetID)
    site_type = get_object_or_404(SiteType, shortname=request.POST.get('type', None))
    fleet.credit_site(site_type, fleet.system, request.user)
    return HttpResponse()


@require_boss()
def remove_site(request, fleetID, siteID):
    """
    Uncredit a site to the given fleet.
    """
    if not request.is_ajax():
        raise PermissionDenied
    fleet = get_object_or_404(Fleet, pk=fleetID)
    site = get_object_or_404(SiteRecord, pk=siteID)
    site.delete()
    return HttpResponse()


@require_boss()
def approve_fleet_site(request, fleetID, siteID, memberID):
    """
    Approve a pending site while the fleet is active.
    """
    if not request.is_ajax():
        raise PermissionDenied
    fleet = get_object_or_404(Fleet, pk=fleetID)
    site = get_object_or_404(SiteRecord, pk=siteID)
    member = get_object_or_404(User, pk=memberID)
    if fleet.ended:
        raise PermissionDenied
    site.members.get(user=member).approve()
    return HttpResponse()


def claim_site(request, fleetID, siteID, memberID):
    """
    Claims the site (making it pending) if called by member.
    Fully grants credit for the site if called by current boss.
    """
    if not request.is_ajax():
        raise PermissionDenied
    fleet = get_object_or_404(Fleet, pk=fleetID)
    site = get_object_or_404(SiteRecord, pk=siteID)
    member = get_object_or_404(User, pk=memberID)

    if fleet.ended:
        raise PermissionDenied

    if fleet.current_boss == request.user:
        site.members.add(UserSite(site=site, user=member, pending=False))
        return HttpResponse()
    elif member == request.user:
        site.members.add(UserSite(site=site, user=member, pending=True))
        return HttpResponse()

    raise PermissionDenied


def unclaim_site(request, fleetID, siteID, memberID):
    """
    Unclaims a site during a running fleet.
    """
    if not request.is_ajax():
        raise PermissionDenied

    fleet = get_object_or_404(Fleet, pk=fleetID)
    site = get_object_or_404(SiteRecord, pk=siteID)
    member = get_object_or_404(User, pk=memberID)

    if fleet.ended:
        raise PermissionDenied

    if fleet.current_boss == request.user or member == request.user:
        site.members.filter(user=member).delete()
        return HttpResponse()

    raise PermissionDenied


