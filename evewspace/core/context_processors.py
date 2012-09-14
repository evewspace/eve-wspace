from django.contrib.sites.models import Site

def site(request):
    current_site = Site.objects.get_current()
    return {'SITE_URL': current_site.domain}
