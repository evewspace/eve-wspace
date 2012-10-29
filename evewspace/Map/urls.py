from django.conf.urls.defaults import patterns, include, url

syspatterns = patterns('Map.views',
        url(r'^$', 'system_details'),
        url(r'^new/$', 'add_system'),
        url(r'^menu/$', 'system_menu'),
        url(r'^tooltip/$', 'system_tooltip'),
        url(r'^interest/$','set_interest'),
        url(r'^location/$', 'manual_location'),
        url(r'^scanned/$', 'mark_scanned'),
        )

wormholepatterns = patterns('Map.views',
        url(r'^tooltip/$', 'wormhole_tooltip'),
        url(r'^$', 'edit_wormhole'),
        )

mappatterns = patterns('Map.views',
        url(r'^$', 'get_map'),
        url(r'^update/$', 'map_checkin'),
        url(r'^refresh/$', 'map_refresh'),
        url(r'^system/(?P<msID>\d+)/', include(syspatterns)),
        url(r'^wormhole/(?P<whID>\d+)/', include(wormholepatterns)),
        )

urlpatterns = patterns('Map.views',
        url(r'^new/$', 'create_map'),
        url(r'^(?P<mapID>\d+)/', include(mappatterns)),
        )
