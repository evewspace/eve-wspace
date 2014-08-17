from django.conf import settings
from core.models import Tenant

class MultitenantMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            request.multitenant_enabled = settings.MULTI_TENANT
            request.default_tenant_enabled = settings.DEFAULT_TENANT_ENABLED
            request.allow_creation = settings.ALLOW_TENANT_CREATION
            current_tenant_id = request.session.get('current_tenant', 1)
            current_tenant = Tenant.objects.get(pk=current_tenant_id)
            request.current_tenant = current_tenant
            request.tenant_list = request.user.tenants
            request.tenant_perms = request.user.tenant_permissions(current_tenant)

