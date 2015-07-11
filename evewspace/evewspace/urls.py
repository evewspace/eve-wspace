#   Eve W-Space
#   Copyright 2014 Andrew Austin and contributors
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from django.conf.urls import patterns, include, url

# Run the autodiscovers for various registries to fill them
from search import registry as search_registry
from Alerts import method_registry
from core import admin_page_registry, nav_registry
# Uncomment to enable django admin
#from django.contrib import admin
#admin.autodiscover()
method_registry.autodiscover()
search_registry.autodiscover()
admin_page_registry.autodiscover()
nav_registry.autodiscover()

# Actual URL definitions
urlpatterns = patterns('',
        # Uncomment the admin/doc line below to enable admin documentation:
        # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
        url(r'^$', 'core.views.home_view', name='index'),
        # Uncommend to enable django admin
        #url(r'^admin/', include(admin.site.urls)),
        url(r'^settings/$', 'core.views.config_view', name='settings'),
        url(r'^account/', include('account.urls')),
        url(r'^map/', include('Map.urls')),
        url(r'^search/', include('search.urls')),
        url(r'^pos/', include('POS.urls')),
        url(r'^sitetracker/', include('SiteTracker.urls')),
        url(r'^alerts/', include('Alerts.urls')),
        url(r'^api/', include('API.urls')),
)
