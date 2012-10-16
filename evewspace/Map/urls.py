from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('', 
        url(r'(?P<mapID>\d+)/$', 'Map.views.get_map', name='get_map'),
        url(r'new/$', 'Map.views.create_map', name='create_map'),
        url(r'system/$', 'Map.views.view_system', {'action': 0}, 'system_ajax'),
        url(r'sysmenu/$', 'Map.views.view_system', {'action': 1}, 'system_menu'),
        url(r'systooltip/$', 'Map.views.view_system', {'action': 2}, 'system_tooltip' ),
        url(r'whtooltip/$', 'Map.views.wormhole_tooltip', name='wormhole_tooltip'),
        url(r'markscanned/$', 'Map.views.mark_scanned', name='mark_scanned'),
        url(r'interest/$', 'Map.views.set_interest', name='interest'),
        url(r'location/$', 'Map.views.assert_location', name='assert_location'),
        )
