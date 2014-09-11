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
from django import template
from django.core.cache import cache
from core.models import NewsFeed
from core.tasks import update_feeds
from datetime import datetime
from time import mktime

register=template.Library()

@register.inclusion_tag('feed.html', takes_context=True)
def feeds(context):
    feeds = []
    for feed in NewsFeed.objects.all():
        if feed.user == context['user'] or feed.user == None:
            feeds.append(feed)
    return {'feeds': feeds}

@register.inclusion_tag('feed_items.html')
def feed_items(feed, retry=False):
    items = []
    data = cache.get('feed_%s' % feed.pk)
    if data:
        try:
            if data == 'error':
                return {'error': True}
            for entry in data['entries']:
                try:
                    dt = datetime.fromtimestamp(mktime(entry['published_parsed']))
                except KeyError:
                    dt = None
                try:
                    url = entry['link']
                except KeyError:
                    url = "#"
                item = {'title': entry['title'].replace('&amp;', '&').replace('&#039;', "'"),
                        'summary': entry['summary'],
                        'time': dt,
                        'url': url}
                items.append(item)
        except Exception:
            return {'error': True}
    if not items and retry == False:
        try:
            update_feeds()
            return feed_items(feed, True)
        except Exception:
            return {'error': True}
    elif  not items and retry == True:
        return {'error': True}
    return {'items': items}
