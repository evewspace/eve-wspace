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
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from method_registry import registry as method_registry
from models import SubscriptionGroup
import tasks

def send_ping(request):
    """"
    GET: Get the send ping dialog.
    POST: Process the send ping dialog.
    """
    if not request.is_ajax():
        raise PermissionDenied
    alert_groups = []
    for group in SubscriptionGroup.objects.all():
        if group.get_user_perms(request.user)[0]:
            alert_groups.append(group)
    if request.method == "POST":
        sub_group = get_object_or_404(SubscriptionGroup, pk=request.POST['alert_group'])
        subject = request.POST.get('alert_subject', '')
        message = request.POST.get('alert_message', '')
        tasks.send_alert.delay(request.user, sub_group, message, subject)
        return HttpResponse()
    else:
        return TemplateResponse(request, "send_ping.html", {'alert_groups': alert_groups})


def edit_subscriptions(request):
    """"
    GET: Get the edit subscritpions dialog.
    POST: Process the edit subscriptions dialog.
    """
    if not request.is_ajax():
        raise PermissionDenied
    # Build a dict of subscribable alert groups as key with list of
    # subscribed methods as info
    current_subs = {}
    available_groups = []
    for sub_group in SubscriptionGroup.objects.all():
        if sub_group.get_user_perms(request.user)[1]:
           available_groups.append(sub_group)
           method_list = []
           for alert_method in method_registry:
               if method_registry[alert_method]().is_registered(request.user, sub_group):
                   method_list.append(alert_method)
           current_subs[sub_group.name] = method_list
    if request.method == "POST":
        for group in available_groups:
            for alert_method in method_registry:
                method_registry[alert_method]().unregister(request.user, group)
                if request.POST.get("%s_%s" % (group.pk, alert_method), False):
                    method_registry[alert_method]().register(request.user, group)
        return HttpResponse()
    else:
        return TemplateResponse(request, "edit_subscriptions.html",
                {'current_subs': current_subs,
                    'all_methods': method_registry,
                    'available_groups': available_groups})

