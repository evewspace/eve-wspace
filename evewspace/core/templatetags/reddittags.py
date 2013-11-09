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

register=template.Library()

@register.inclusion_tag('reddit_list.html')
def reddit_list():
    if cache.get('reddit'):
        try:
            return {'reddit_data': cache.get('reddit')['data']['children']}
        except Exception:
            return {'error': True}
    else:
        return {'error': True}

@register.inclusion_tag('reddit_item.html')
def reddit_item(item):
    score = int(item['data']['ups']) - int(item['data']['downs'])
    comment_link = "%s%s" % ("http://www.reddit.com", item['data']['permalink'])
    return {'upvotes': item['data']['ups'], 'downvotes': item['data']['downs'],
            'target_url': item['data']['url'], 'author': item['data']['author'],
            'score': score, 'comments': item['data']['num_comments'],
            'comment_url': comment_link, 'title': item['data']['title']}
