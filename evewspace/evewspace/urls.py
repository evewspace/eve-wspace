from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import autocomplete_light
autocomplete_light.autodiscover()
admin.autodiscover()
#django_cron.autodiscover()
urlpatterns = patterns('',
        # Examples:
        # url(r'^$', 'eve-space.views.home', name='home'),
        # url(r'^WormholeSpace2/', include('eve-space.foo.urls')),

        # Uncomment the admin/doc line below to enable admin documentation:
        # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
        url(r'^$', 'core.views.home_view', name='index'),
        url(r'^account/', include('account.urls')),
        url(r'^map/', include('Map.urls')),
        # Uncomment the next line to enable the admin:
         url(r'^sekrit/', include(admin.site.urls)),
         url(r'autocomplete/', include('autocomplete_light.urls')),
)
