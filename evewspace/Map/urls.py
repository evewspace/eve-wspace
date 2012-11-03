from django.conf.urls.defaults import patterns, include, url

sigpatterns = patterns('Map.views',
        )

syspatterns = patterns('Map.views',
        url(r'^$', 'system_details'),
        url(r'^menu/$', 'system_menu'),
        url(r'^tooltip/$', 'system_tooltip'),
        url(r'^interest/$','set_interest'),
        url(r'^location/$', 'manual_location'),
        url(r'^scanned/$', 'mark_scanned'),
        url(r'^signatures/$', 'get_signature_list'),
        url(r'^signatures/new/$', 'add_signature'),
        url(r'^signatures/(?P<sigID>\d+)/', include(sigpatterns)),
        )

wormholepatterns = patterns('Map.views',
        url(r'^tooltip/$', 'wormhole_tooltip'),
        url(r'^$', 'edit_wormhole'),
        )

mappatterns = patterns('Map.views',
        url(r'^$', 'get_map'),
        url(r'^update/$', 'map_checkin'),
        url(r'^refresh/$', 'map_refresh'),
        url(r'^system/new/$', 'add_system'),
        url(r'^system/(?P<msID>\d+)/', include(syspatterns)),
        url(r'^wormhole/(?P<whID>\d+)/', include(wormholepatterns)),
        )

urlpatterns = patterns('Map.views',
        url(r'^new/$', 'create_map'),
        url(r'^(?P<mapID>\d+)/', include(mappatterns)),
        )
