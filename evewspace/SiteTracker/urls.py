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


fleetmembersitepatterns = patterns('SiteTracker.views',
        url(r'unclaim/$', 'unclaim_site'),
        url(r'claim/$', 'claim_site'),
        )

fleetsitepatterns = patterns('SiteTracker.views',
        url(r'delete/$', 'remove_site'),
        url(r'member/(?P<memberID>\d+)/', include(fleetmembersitepatterns)),
        )

fleetmemberpatterns = patterns('SiteTracker.views',
        url(r'kick/$', 'kick_member'),
        url(r'promote/$', 'promote_member'),
        url(r'$', 'refresh_boss_member'),
        )

fleetpatterns = patterns('SiteTracker.views',
        url(r'join/$', 'join_fleet'),
        url(r'leave/$', 'leave_fleet'),
        url(r'site/$', 'credit_site'),
        url(r'bosspanel/$', 'boss_panel'),
        url(r'site/(?P<siteID>\d+)/', include(fleetsitepatterns)),
        url(r'member/(?P<memberID>\d+)/', include(fleetmemberpatterns)),
        url(r'disband/$', 'disband_fleet'),
        )

urlpatterns = patterns('SiteTracker.views',
        url(r'fleet/new/$', 'create_fleet'),
        url(r'fleet/leaveall/$', 'leave_fleet'),
        url(r'fleet/$', 'refresh_fleets'),
        url(r'fleet/(?P<fleetID>\d+)/', include(fleetpatterns)),
        url(r'status/$', 'st_status'),
        url(r'$', 'status_bar'),
        )
