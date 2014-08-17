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
from django.contrib.sites.models import Site
from core.models import Tenant
from django.conf import settings

def site(request):
    current_site = Site.objects.get_current()
    return {'SITE_URL': current_site.domain}

def multitenant(request):
    if request.user.is_authenticated():
        multitenant_enabled = settings.MULTI_TENANT
        default_tenant_enabled = settings.DEFAULT_TENANT_ENABLED
        if default_tenant_enabled:
            default_tenant = Tenant.objects.get(pk=1)
        else:
            default_tenant = None
        allow_creation = settings.ALLOW_TENANT_CREATION
        current_tenant_id = request.session.get('current_tenant', 1)
        current_tenant = Tenant.objects.get(pk=current_tenant_id)
        tenant_list = request.user.tenants
        tenant_perms = request.user.tenant_permissions(current_tenant)
        return {'multitenant_enabled': multitenant_enabled,
                'default_tenant_enabled': default_tenant_enabled,
                'current_tenant': current_tenant,
                'tenant_list': tenant_list,
                'tenant_perms': tenant_perms,
                'allow_creation': allow_creation,
                'default_tenant': default_tenant}
    else:
        return {}
