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
from celery import task
from django.core.cache import cache
import urllib
import json

@task()
def cache_eve_reddit():
    """
    Attempts to cache the top submissions to r/Eve.
    """
    current = cache.get('reddit')
    if not current:
        # No reddit data is cached, grab it.
        data = json.loads(urllib.urlopen('http://www.reddit.com/r/Eve/top.json').read())
        cache.set('reddit', data, 120)
    else:
        # There is cached data, let's try to update it
        data = json.loads(urllib.urlopen('http://www.reddit.com/r/Eve/top.json').read())
        if 'data' in data:
            # Got valid response, store it
            cache.set('reddit', data, 120)
        else:
            # Invalid response, refresh current data
            cache.set('reddit', current, 120)
