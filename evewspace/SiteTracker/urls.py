#    Eve W-Space
#    Copyright (C) 2013  Andrew Austin and other contributors
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version. An additional term under section
#    7 of the GPL is included in the LICENSE file.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
from django.conf.urls.defaults import patterns, include, url


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
        url(r'$', 'status_bar'),
        )
