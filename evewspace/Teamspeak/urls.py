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
from django.conf.urls import patterns,include, url

settingspatterns = patterns('Teamspeak.views',
        url(r'^general/$', 'general_settings'),
        )

urlpatterns = patterns('Teamspeak.views',
        url(r'show_online/$', 'show_online'),
        url(r'^settings/', include(settingspatterns)),
        )
