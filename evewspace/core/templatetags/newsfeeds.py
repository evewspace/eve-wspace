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
