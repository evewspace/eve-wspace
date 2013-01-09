from django.conf.urls.defaults import patterns, include, url

sigpatterns = patterns('Map.views',
        url(r'^activate/$', 'activate_signature'),
        url(r'^escalate/$', 'escalate_site'),
        url(r'^clear/$', 'mark_signature_cleared'),
        url(r'^remove/$', 'delete_signature'),
        url(r'^edit/$', 'edit_signature'),
        url(r'^spawns/$', 'site_spawns')
        )

syspatterns = patterns('Map.views',
        url(r'^$', 'system_details'),
        url(r'^menu/$', 'system_menu'),
        url(r'^tooltip/$', 'system_tooltip'),
        url(r'^interest/$','set_interest'),
        url(r'^location/$', 'manual_location'),
        url(r'^scanned/$', 'mark_scanned'),
        url(r'^remove/$', 'remove_system'),
        url(r'^edit/$', 'edit_system'),
        url(r'^destinations/$', 'destination_list'),
        url(r'^addchild/$', 'manual_add_system'),
        url(r'^signatures/$', 'get_signature_list'),
        url(r'^signatures/new/$', 'add_signature'),
        url(r'^signatures/bulkadd/$', 'bulk_sig_import'),
        url(r'^signatures/(?P<sigID>\d+)/', include(sigpatterns)),
        )

wormholepatterns = patterns('Map.views',
        url(r'^tooltip/$', 'wormhole_tooltip'),
        url(r'^edit/$$', 'edit_wormhole'),
        )

mappatterns = patterns('Map.views',
        url(r'^$', 'get_map'),
        url(r'^update/$', 'map_checkin'),
        url(r'^refresh/$', 'map_refresh'),
        url(r'^edit/$', 'edit_map'),
        url(r'^delete/$', 'delete_map'),
        url(r'^system/new/$', 'add_system'),
        url(r'^system/(?P<msID>\d+)/', include(syspatterns)),
        url(r'^wormhole/(?P<whID>\d+)/', include(wormholepatterns)),
        url(r'^settings/$', 'map_settings'),
        )

spawnspatterns = patterns('Map.views',
        url(r'^edit/$', 'edit_spawns'),
        url(r'^delete/$', 'delete_spawns'),
        )

sigtypepatterns = patterns('Map.views',
        url(r'^edit/$', 'edit_sigtype'),
        url(r'^delete/$', 'delete_sigtype'),
        )

settingspatterns = patterns('Map.views',
        url(r'^general/$', 'general_settings'),
        url(r'^sitespawns/$', 'sites_settings'),
        url(r'^permissions/$', 'global_permissions'),
        url(r'^sitespawns/add/$', 'add_spawns'),
        url(r'^sitespawns/(?P<spawnID>\d+)/', include(spawnspatterns)),
        url(r'^destinations/$', 'destination_settings'),
        url(r'^destinations/new/$', 'add_destination'),
        url(r'^destinations/(?P<destID>\d+)/delete/$', 'delete_destination'),
        url(r'^sigtypes/$', 'sigtype_settings'),
        url(r'^sigtypes/(?P<sigtypeID>\d+)/', include(sigtypepatterns)),
        )

urlpatterns = patterns('Map.views',
        url(r'^new/$', 'create_map'),
        url(r'^(?P<mapID>\d+)/', include(mappatterns)),
        url(r'^settings/', include(settingspatterns)),
        )
