from django.core.cache import cache
import time
import zlib
import cPickle as pickle
from datetime import datetime
import pytz


def store(host, path, params, doc, obj):
    """Store an API document in our cache."""
    #First remove any outdated versions of the document.
    cacheKey = "%s%s%s" %(host, path, params)
    cache.set(hash(cacheKey), zlib.compress(pickle.dumps(obj)), obj.cachedUntil - int(time.time()))


def retrieve(host, path, params):
    """Get an API document from our cache."""
    cacheKey = "%s%s%s" % (host, path, params)
    if cache.get(hash(cacheKey)):
        return pickle.loads(zlib.decompress(cache.get(hash(cacheKey))))
    else:
        return None

def timestamp_to_datetime(timestamp):
    """Converts a UNIX Timestamp (in UTC) to a python DateTime"""
    result = datetime.fromtimestamp(timestamp).replace(tzinfo=pytz.utc)
    return result
