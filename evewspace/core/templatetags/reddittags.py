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
