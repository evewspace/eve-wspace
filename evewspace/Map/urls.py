from django.conf.urls.defaults import patterns, include, url

syspatterns = patterns('Map.views',
        url(r'^$', 'system_details'),
        url(r'^menu/$', 'system_menu'),
        url(r'^tooltip/$', 'system_tooltip'),
        )

mappatterns = patterns('Map.views',
        url(r'^$', 'get_map'),
        url(r'^system/(?P<sysID>\d+/', include(syspatterns)),
        )

urlpatterns = patterns('Map.views',
        url(r'^new/$', 'create_map'),
        url(r'^(?P<mapID>\d+)/', include(mappatterns),
        )

#urlpatterns = patterns('Map.views', 
#        url(r'whtooltip/$', 'Map.views.wormhole_tooltip', name='wormhole_tooltip'),
#        url(r'markscanned/$', 'Map.views.mark_scanned', name='mark_scanned'),
#        url(r'interest/$', 'Map.views.set_interest', name='interest'),
#        url(r'location/$', 'Map.views.assert_location', name='assert_location'),
#        )
