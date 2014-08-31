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
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from Map.models import Map
from core.models import Tenant
from django.template.response import TemplateResponse

# Create your views here.

@login_required()
def home_view(request):
    """The home view detects whether a user has a default map and either
    directs them to that map or displays a home page template."""

    return TemplateResponse(request, 'home.html')


@login_required()
def switch_tenant(request, tenant_id):
    old_tenant = request.current_tenant
    new_tenant = get_object_or_404(Tenant, pk=tenant_id)
    if new_tenant not in request.user.tenants:
        raise PermissionDenied

    request.session['current_tenant'] = new_tenant.pk
    return HttpResponseRedirect(reverse('index'))


@login_required
def config_view(request):
    """
    Gets the configuration page.
    """
    return TemplateResponse(request, 'settings.html')
