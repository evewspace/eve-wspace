from django.conf.urls.defaults import patterns, include, url

syspatterns = patterns('Map.views',
        url(r'^$', 'system_details'),
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
        url(r'^system/(?P<msID>\d+)/', include(syspatterns)),
        url(r'^wormhole/(?P<whID>\d+)/', include(wormholepatterns)),
        )

urlpatterns = patterns('Map.views',
        url(r'^new/$', 'create_map'),
        url(r'^(?P<mapID>\d+)/', include(mappatterns)),
        )

#urlpatterns = patterns('Map.views', 
#        url(r'whtooltip/$', 'Map.views.wormhole_tooltip', name='wormhole_tooltip'),
#        url(r'markscanned/$', 'Map.views.mark_scanned', name='mark_scanned'),
#        url(r'interest/$', 'Map.views.set_interest', name='interest'),
#        url(r'location/$', 'Map.views.assert_location', name='assert_location'),
#        )
