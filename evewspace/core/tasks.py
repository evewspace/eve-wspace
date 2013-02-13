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
